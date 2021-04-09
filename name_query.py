"""
    CS051P Lab Assignments: BabiesSQL

    Author: Charles Rak
    Partner: Theo Brown

    Date:  November 10 2020

    The goal of this assignment is to give you more practice with data 
    management and analysis via database.
"""
import sqlite3
import os
import sys
from sqlite3 import Error

postcodes = dict()

def run_query(conn, name, state):
    """
    :param conn: sql object connection
    :param name: name pattern
    :param state: state postcode
    :return : first list of data
    """
    # Selects the necesssary data from the query
    sql_query = """SELECT count, year, name, postcode FROM names, counts WHERE name like '{0}' AND names.nameID == counts.nameID and postcode == '{1}'
                """
    cur = conn.cursor()
    # change wildcard character from * to %
    name = name.replace('*','%')
    cur.execute(sql_query.format(name, state))
    rows = cur.fetchall()
    return list(rows)

def create_postcode_dictionary(postcode_file):
    """
    Builds a postal code dictionary from the postcode file
    :param postcode_file: (str) the name of postcode file
    : return: None
    """
    file_in = open(postcode_file, "r")
    # Cycles through lines in file_in
    for line in file_in:
        # Splits each line into a list by comma
        postal_codes = line.split(",")
        # Assigns the state postcode key to the state name value in a dictionary
        postcodes[postal_codes[1]] = postal_codes[0]
        


def validate_pattern(pattern):
    """ Validate name pattern   Abce[*]
    :param name: name string to validate
    :return error: string if error or '' if no error
    """
    # If pattern ends with a star, then it can be 16 characters long
    if pattern[-1] == "*":
        if not pattern[0].isupper() or len(pattern) > 16:
            return "Error"
    #  Otherwise it can only be 15
    # Both cases require first letter to be uppercase
    elif not pattern[0].isupper() or len(pattern) > 15:
        return "Error"

    else:
        return ''

def validate_postcode(state):
    """
    Check if postcode is in dictionary
    :input state: state postcode
    :return boolean: True if legal, otherwise False
    """
    # Checks if the state postcode is in postcodes
    return state in postcodes

def init(dbfile,pcfile):
    """
    Initialize data structures
    :input dbfile: the database file
    :input pcfile: the postcode file
    """
    try:
        conn = sqlite3.connect(dbfile)
    except Error as e:
        sys.exit(e)

    create_postcode_dictionary(pcfile)
    return conn

def main(conn):
    """
    Inputs a name pattern and a postcode, prints out the first 10 rows of data
    or prints an error string if the inputs failed validation
    :input conn: database connection
    """

    pattern = input("Name pattern:\n\t")
    
    error = validate_pattern(pattern)
    if error:
        print(error)
        return
    state = input("State:\n\t")
    error = validate_postcode(state)
    if error:
        print(error)
        return
    
    rows = run_query(conn, pattern, state)
    # print(rows)
    for r in rows[:5]:
        print(r[0],r[1])
    
if __name__ == "__main__":
    if len(sys.argv) > 2:
        conn = init(sys.argv[1],sys.argv[2])
    else:
        conn = init('./babies.db','./PostalCodes.txt')
    main(conn)
