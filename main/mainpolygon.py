import osdb
import time
from flask import Flask
import random
import sys
import pymysql
from opensky_api import OpenSkyApi
#import pyModeS
import django.forms
#help(django.forms)
#from ipware import get_client_ip


OPENSKY_USER_NAME = "Grinevski"
OPENSKY_PASSWORD = "myflightradar2022"
DB_NAME = 'open_sky_db_2022'
DB_ROOT_PASSWORD = 'FR21072022con'

LAST_DB_UPDATE_TIME = 0
DB = 0

def open_sky_connection():
    print('Connecting to Open sky API...')
    try:
        con = OpenSkyApi(OPENSKY_USER_NAME, OPENSKY_PASSWORD)
        print('Connection is successful!')
        return con
    except:
        print('Connection to Open sky APY failed! Please check your internet connection.')
        return None

def db_connection(hst, usr, pwd, database):
    print('Connecting to MySQL database...')
    try:
        con = pymysql.connect(host = hst, user = usr, password = pwd)
        print("Connection is successful!")
        return con
    except:
        print('Connection failed.')
        return None

#print("Matthias Schäfer, Martin Strohmeier, Vincent Lenders, Ivan Martinovic and Matthias Wilhelm. Bringing Up OpenSky: A Large-scale ADS-B Sensor Network for Research. In Proceedings of the 13th IEEE/ACM International Symposium on Information Processing in Sensor Networks (IPSN), pages 83-94, April 2014.")


def main():
    api_con = open_sky_connection()
    db_con = db_connection('localhost', 'root', DB_ROOT_PASSWORD, DB_NAME)
    if api_con != None and db_con != None:
#        prepare_states_db(db_con)
        if time.time() - LAST_DB_UPDATE_TIME > 600:
            print('The aircraft state vectors database is not up to date. Update is in process...')
#            osdb.update_states_db(api_con, db_con)
    else:
        print('Coud not connect to either Opensky resource or main database. Please try again later.')

    mycursor = db_con.cursor()
    osdb.show_all_tables(db_con, "open_sky_db_2022")
    osdb.show_columns(db_con, "open_sky_db_2022", "main_state")
#    osdb.update_states_db(api_con, db_con)    
#    osdb.show_table_data(db_con, "open_sky_db_2022", "accounts_customuser")
    osdb.plot_speed_at_alt_range(db_con, DB_NAME, 0, 15000)    

    print()
#    osdb.show_columns(db_con, "open_sky_db_2022", "main_position_source")
    print()
#    osdb.show_columns(db_con, "open_sky_db_2022", "main_category")

main()
