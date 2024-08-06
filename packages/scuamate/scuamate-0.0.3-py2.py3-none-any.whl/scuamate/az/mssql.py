# mssql.py

from datetime import datetime
import numpy as np
import pandas as pd
import geopandas as gpd
import pyodbc
import pprint
import re
import os

from ..core import get_prev_utc_datetime as _get_prev_utc_datetime
from ..core import get_dotenv_vals as _get_dotenv_vals
from ..core import InvalidPointsError as InvalidPointsError
from .. import az as _az

##########
# FN DEFS:

def get_formatted_prev_utc_time(**kwargs):
    '''
    get a properly formatted timestamp for some amount of time ago
    (using kwargs fed to `datetime.datetime.timedelta`),
    '''
    dt = _get_prev_utc_datetime(**kwargs)
    assert isinstance(dt, datetime)
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def prep_conn_info_dict(sql_server_name,
                       sql_db_name,
                       sql_db_uid,
                       sql_pwd,
                      ):
    '''
    put all the info necessary for creating a SQL connection object into a dict
    '''
    conn_info =  {'sql_server_name': sql_server_name,
                  'sql_db_name': sql_db_name,
                  'sql_db_uid': sql_db_uid,
                  'sql_pwd': sql_pwd,
                 }
    return conn_info


def get_access_info(dotenv_filename,
                    servername_dotenv_val,
                    dbname_dotenv_val,
                    username_dotenv_val,
                    secretname_dotenv_val,
                    azure_vault_name,
                   ):
    '''
    read the MSSQL server name ('servername_dotenv_val'),
    database name ('dbname_dotenv_val'),
    user name ('username_dotenv_val'),
    and Azure KeyVault secret name ('secretname_dotenv_val')
    from the given dotenv-file ('dotenv_filename'),
    get the password from the given Azure KeyVault
    ('azure_vault_name'),
    then use all of that info to retrieve and return
    the formatted information needed for access to the MSSQL database
    (a dict containing the server name, database name, user name, and password)
    '''
    (secret_name,
     server_name,
     db_name,
     db_uid,
    ) = _get_dotenv_vals(dotenv_filename,
                        [secretname_dotenv_val,
                         servername_dotenv_val,
                         dbname_dotenv_val,
                         username_dotenv_val,
                        ],
                       )
    pwd = _az.keyvault.get_secret(azure_vault_name, secret_name)
    # prep SQL connection info
    acc_info = prep_conn_info_dict(server_name,
                                   db_name,
                                   db_uid,
                                   pwd,
                                  )
    return acc_info


def verify_conn_info_contents(conn_info):
    '''
    check that a conn_info dict has the right contents
    '''
    assert isinstance(conn_info, dict)
    for k in ['sql_server_name', 'sql_db_name', 'sql_db_uid', 'sql_pwd']:
        assert k in conn_info.keys()


def connect_to_db(conn_info,
                  driver_str='{ODBC Driver 18 for SQL Server}'):
    '''
    create a connection object to an MS SQL database
    '''
    # verify the contents of the connection info dict
    verify_conn_info_contents(conn_info)
    # create and return the connection
    conn_str = (f"Driver={driver_str};"
                f"Server=tcp:{conn_info['sql_server_name']}"
                 ".database.windows.net,1433;"
                f"Database={conn_info['sql_db_name']};"
                f"Uid={conn_info['sql_db_uid']};"
                f"Pwd={conn_info['sql_pwd']};"
                 "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    conn = pyodbc.connect(conn_str)
    return conn


def insert_data(insert_cmd,
                conn_info=None,
                conn=None,
               ):
    '''
    use the given MS SQL insert command,
    and the given connection info or object,
    to insert data into the db
    '''
    assert re.search('INSERT', insert_cmd) is not None, ('The given command '
                                                         'does not appear to '
                                                         'be an INSERT!')
    assert (conn_info is not None) or (conn is not None), ("Either "
                "'conn_info' or 'conn' must be provided.")
    if conn is None:
        with connect_to_db(conn_info) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_cmd)
            cursor.close()
    else:
        cursor = conn.cursor()
        cursor.execute(insert_cmd)
        cursor.close()
    return


def get_data(sql_cmd,
             conn_info=None,
             conn=None,
            ):
    '''
    use the given MS SQL command,
    and the given connection info or object,
    to pull data from the db
    '''
    assert (conn_info is not None) or (conn is not None), ("Either "
                "'conn_info' or 'conn' must be provided.")
    if conn is None:
        with connect_to_db(conn_info) as conn:
            df = pd.read_sql(sql=sql_cmd, con=conn)
    else:
        df = pd.read_sql(sql=sql_cmd, con=conn)
    return df


def get_points(sql_cmd,
               conn_info=None,
               conn=None,
              ):
    '''
    use the given MS SQL db and table info, and the given SQL command,
    to pull and validate a `geopandas.GeoDataFrame` of spatial points data
    '''
    df = get_data(sql_cmd,
                  conn_info=conn_info,
                  conn=conn,
                 )
    assert isinstance(df, pd.DataFrame)
    try:
        pts = gpd.GeoDataFrame(df,
                               geometry=gpd.points_from_xy(df.Longitude,
                                                           df.Latitude,
                                                          ),
                               crs='EPSG:4326')
    # check data can be coerced to points gdf
    except Exception as e:
        raise InvalidPointsError('MS SQL database', e)
    return pts


def insert_vals_into_tbl(data,
                         tbl_name,
                         cursor,
                         field_names=None,
                         output_field=None,
                         debug=False,
                        ):
    '''
    insert the given data into the indicated table in the
    database of the given cursor object

    data can be provided as either a pandas.DataFrame or a dict of
    field:value pairs (where value can be either a single value or an iterable
    containing multiple values, in which can each field must have the same
    number of values to be inserted)

    Table to be inserted into must have the same column structure as the
    DataFrame given (minus any self-implementing primary key fields, etc.)

    It is assumed that SQL field names match the column names in the table, so
    if they do not then provide the SQL field names to the 'field_names' arg as a list.

    The post-insert value of a field (e.g., and auto-incremented primary key)
    can be returned using the OUTPUT statment, if desired, by setting
    output_field to the name of the field whose value should be output.
    Otherwise nothing is output.
    '''
    # prep the values to be inserted
    if isinstance(data, dict):
        if not np.all([isinstance(v, list) for v in data.values()]):
            data = {k: [v] for k, v in data.items()}
        data = pd.DataFrame.from_dict(data)
    # grab the field names
    if field_names is None:
        field_names = [*data.columns]
    # set up the output statement and output data structure, if requested
    if output_field is not None:
        output_str = f' OUTPUT INSERTED.{output_field} '
        output_vals = []
    else:
        output_str = ''
    # iterate over the devices df and insert each row into the devices table
    insert_ct = 0
    for i, row in data.iterrows():
        row_dict = row.to_dict()
        # get col names and formatted values
        vals = []
        for val in row_dict.values():
            if pd.isnull(val): # NOTE: this will catch pd.NaT as well as np.NaN
                vals.append('NULL')
            elif isinstance(val, pd._libs.tslibs.timestamps.Timestamp):
                vals.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
            elif isinstance(val, str):
                if re.search('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\+00:00)?', val):
                    vals.append(f"'{str(val).split('+')[0].replace(' ', 'T')}'")
                else:
                    vals.append(f"'{val}'")
            # NOTE: bools must be expressed as '0'|'1' (for BIT field);
            #       otherwise throws an error
            elif isinstance(val, bool):
                vals.append(str(int(val)))
            else:
                vals.append(f"{val}")
        # format the full INSERT command
        insert_cmd = """
            INSERT INTO {} ({}){}VALUES ({})
            """.format(tbl_name,
                       ", ".join(field_names),
                       output_str,
                       ", ".join(vals))
        res = cursor.execute(insert_cmd)
        insert_ct += 1
        if output_field is not None:
            output_val = res.fetchall()
            assert len(output_val) == 1
            output_vals.append(output_val[0])
    if debug:
        print((f"\t\tinserted {insert_ct} row{'s' * (len(data)>1)} into {tbl_name}; "
               'check results, then commit'))
    if output_field is not None:
        return output_vals
    else:
        return


def write_schema_dbml(conn_info,
                      dbml_filename='schema.dbml',
                      overwrite=False,
                     ):
    '''
    connect to a database and return a DBML representation of all of its tables
    NOTE: CURRENTLY REQUIRES KEYS TO BE MANUALLY WRITTEN INTO OUTPUT FILE
    '''
    with connect_to_db(conn_info) as conn:
        # start DBML str
        dbml = ''
        # get all tables
        tables_cmd = 'SELECT * FROM INFORMATION_SCHEMA.TABLES'
        tables = get_data(tables_cmd, conn=conn)
        for table in tables[tables['TABLE_TYPE'] == 'BASE TABLE']['TABLE_NAME']:
            dbml += f'Table {table} ' + '{\n'
            cols_cmd = ("SELECT COLUMN_NAME, DATA_TYPE "
                        "FROM INFORMATION_SCHEMA.COLUMNS "
                       f"WHERE TABLE_NAME='{table}'")
            cols = get_data(cols_cmd, conn=conn)
            for i, row in cols.iterrows():
                col = row['COLUMN_NAME']
                dt = row['DATA_TYPE']
                dbml += f'  {col} {dt}\n'
            dbml += '}\n\n'
    assert not os.path.isfile(dbml_filename) or overwrite, ('DBML file could '
                                                            'not be written! '
                                                            'File exists and '
                                                            'overwrite==False.')
    with open(dbml_filename, 'w') as f:
        f.write(dbml)

