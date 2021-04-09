"""
Author: Geoffrey Brown

Create a data base using census baby names data.  Those data are in files named AK.TXT,AL.TXT ...
A typical file contains data of the form:

    AK,F,1910,Mary,14
    AK,F,1910,Annie,12
    AK,F,1910,Anna,10
    AK,F,1910,Margaret,8
    AK,F,1910,Helen,7
    AK,F,1910,Elsie,6
    AK,F,1910,Lucy,6
    AK,F,1910,Dorothy,5

Where the data is of the form:

   Postal Code,Gender,Year,Name,Count

This program creates a database with two tables

    names:  (id,name)
    counts: (id,year,count,gender,postcode,name_id)

"""


import sqlite3
import os
import glob
import time
import sys
from sqlite3 import Error

DBFileName = "babies.db"

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        sys.exit(e)

def create_connection(db_file):
    """ create a database connection to a SQLite database 
    :param db_file: Path of file to create
    :return conn: connection object
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        sys.exit(e)

    return conn
    
def create_names_table(conn):
    """ Create names table
    :param conn: database connection object
    """
    sql_create_names_table = """ CREATE TABLE IF NOT EXISTS names (
                                        NameId integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """
    create_table(conn,sql_create_names_table)

def create_data_table(conn):
    """ Create data table
    :param conn: database connection object
    """
    sql_create_data_table = """ CREATE TABLE IF NOT EXISTS counts (
                                        CountId integer PRIMARY KEY,
                                        year  integer NOT NULL,
                                        count integer NOT NULL,
                                        gender text NOT NULL,
                                        postcode text NOT NULL,
                                        NameId integer NOT NULL,
                                        FOREIGN KEY (NameId) REFERENCES names(NameId)
                                    ); """
    create_table(conn,sql_create_data_table)

def insert_data(conn,datapath):
    """ Insert data into database; updates data table and names table
    :param conn: database connection object
    :param datapath: directory path for babies files (AK.TXT,...)
    :return:
    """

    name_dict = dict()
    name_id = 1
    name_files = glob.glob(datapath + "/*.TXT")
    cur = conn.cursor()
    rows = 0

    # Walk through data files and insert data in count_table;
    # Build names dictionary as we go

    sql = ''' INSERT INTO counts(year,count,gender,postcode,NameId)
              VALUES(?,?,?,?,?) '''
    
    for n in name_files:  
        with open(n,'r') as f:
            for d in f:
                state,gender,year,name,count = d.strip().split(",")
                # Lookup name id
                if not name in name_dict:
                    name_dict[name] = name_id
                    name_id = name_id + 1
                # insert data in count_table
                cur.execute(sql,[year,count,gender,state,name_dict[name]])
                rows += 1
        # commit after every state
        conn.commit()

    print("Inserted",rows,"items into data table")
   
    # Now insert names.  In this case, we use the primary
    # created in the names directory

    sql = ''' INSERT INTO names(NameId,name) VALUES(?,?) '''

    for k in name_dict.keys():
        cur.execute(sql,[name_dict[k],k])

    conn.commit()
    print("Unique Names:", cur.lastrowid)

def build_database(dbname,datapath):
    """
    build the names database
    :param dbname: path to database file to create/recreate
    :param datapath: path to directory containing names data files
    :param pcfile: path to file containing postal codes
    """
    
    if os.path.exists(dbname):
        os.remove(dbname)
    conn = create_connection(dbname)

    if conn is not None:
        create_names_table(conn)
        create_data_table(conn)
        insert_data(conn,datapath)
    else:
        print("Error! cannot create the database connection.")
        return None
    return conn

if __name__ == "__main__":
    start = time.time()
    build_database(DBFileName,'./namesbystate')
    print("Elapsed Time", time.time() - start)  