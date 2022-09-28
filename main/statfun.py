import pymysql
import time

import matplotlib.pyplot as plt
import io
import urllib, base64

def chart_by_par(tab, par1, par2, date_from, date_to):
    speed_lst = []
    geo_alt_lst = []
    for state in tab:
        speed_lst.append(state.velocity)
        geo_alt_lst.append(state.geo_altitude)
    plt.plot(geo_alt_lst, speed_lst)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)

    return url
  

def prepare_states_db(db_con):
    mycursor = db_con.cursor()
#    mycursor.execute("DROP DATABASE IF EXISTS open_sky_db_2022")

#    mycursor.execute("SHOW DATABASES")
#    print('These are available databases:')
#    for x in mycursor:
#        print(x)
#    print()
    
    mycursor.execute("CREATE DATABASE IF NOT EXISTS open_sky_db_2022")
    mycursor.execute("USE open_sky_db_2022")

    sql_states = '''CREATE TABLE IF NOT EXISTS webflightdog_state(  
        state_id INT AUTO_INCREMENT PRIMARY KEY,
        icao24 VARCHAR(10),
        callsign VARCHAR(10),
        origin_country VARCHAR(45),
        time_position INT(45),
        last_contact INT(15),
        longitude FLOAT(45),
        latitude FLOAT(45),
        geo_altitude DECIMAL(10),
        on_ground VARCHAR(5), 
        velocity DECIMAL(45),
        true_track DECIMAL(10),
        vertical_rate DECIMAL(10),
        sensors VARCHAR(45),
        baro_altitude DECIMAL(10),
        squawk VARCHAR(45),
        spi VARCHAR(45),
        position_source_id INT(5)),
        category_id,
        PRIMARY KEY (state_id),
        FOREIGN KEY (category_id) REFERENCES categories(category_id))'''
    mycursor.execute(sql_states)

    sql_users = '''CREATE TABLE IF NOT EXISTS users(
        user_ID INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(45),
        last_name VARCHAR(45),
        DoB DATE,
        password VARCHAR(45),
        last_IP VARCHAR(45),
        country VARCHAR(45),
        fav_flight VARCHAR(45))'''
    mycursor.execute(sql_users)

    sql_countries = '''CREATE TABLE IF NOT EXISTS countries(
        country_ID INT AUTO_INCREMENT PRIMARY KEY,
        country_name VARCHAR(45))'''
    mycursor.execute(sql_countries)

#    print()
#    print('Existing tables:')
#    mycursor.execute("USE open_sky_db_2022")
#    mycursor.execute("SHOW TABLES")
#    for x in mycursor:
#        print(x)
#    print()
        
#    print('These are available databases:')
#    mycursor.execute("SHOW DATABASES")
#    for x in mycursor:
#        print(x)
        
#    print()
#    mycursor.execute("USE open_sky_db_2022")
#    mycursor.execute("SHOW COLUMNS FROM states")
#    for x in mycursor:
#        print(x)
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

def for_v(par):
    if par == None:
        return str(0)
    else:
        return str(par)

def show_all_tables(db_con, db):
    mycursor = db_con.cursor()
    mycursor.execute("USE " + db)
    mycursor.execute("SHOW TABLES")
    print('Tables in database ' + db + ':')
    for x in mycursor:
        print(x)
    print()

def show_columns(db_con, db, tab):    
    mycursor = db_con.cursor()
    mycursor.execute("USE " + db)
    mycursor.execute("SHOW COLUMNS FROM " + tab)
    print('Columns in table ' + tab + ':')
    for x in mycursor:
        print(x)
    print()    

def show_table_data(db_con, db, tab):    
    mycursor = db_con.cursor()
    mycursor.execute("USE " + db)
    mycursor.execute("SELECT * FROM " + tab)
    print('Data in table ' + tab + ':')
    for row in mycursor.fetchall():
        print(row)
    print()    

def populate_ps(api_con, db_con):
    mycursor = db_con.cursor()
    mycursor.execute("USE open_sky_db_2022")
#    mycursor.execute("DELETE FROM main_position_source")
    sql1 = "INSERT INTO main_position_source(id, position_source) VALUES(1, 'ASTERIX')"
    sql2 = "INSERT INTO main_position_source(id, position_source) VALUES(2, 'MLAT')"
    sql3 = "INSERT INTO main_position_source(id, position_source) VALUES(3, 'FLARM')"
    sql4 = "INSERT INTO main_position_source(id, position_source) VALUES(4, 'ADS-B')"

    mycursor.execute("ALTER TABLE main_position_source AUTO_INCREMENT=0")
    mycursor.execute(sql1)
    print(sql1)
    db_con.commit()
    mycursor.execute(sql2)
    print(sql2)
    mycursor.execute(sql3)
    print(sql3)
    mycursor.execute(sql4)
    print(sql4)
    db_con.commit()
    print('Position sources table has been populated with 4 records.')

def populate_category(api_con, db_con):
    mycursor = db_con.cursor()
    mycursor.execute("USE open_sky_db_2022")
#    mycursor.execute("DELETE FROM main_position_source")
    sql1 = "INSERT INTO main_category(id, category) VALUES(1, 'No ADS-B Emitter Category Information')"
    sql2 = "INSERT INTO main_category(id, category) VALUES(2, 'Light (< 15500 lbs)')"
    sql3 = "INSERT INTO main_category(id, category) VALUES(3, 'Small (15500 to 75000 lbs)')"
    sql4 = "INSERT INTO main_category(id, category) VALUES(4, 'Large (75000 to 300000 lbs)')"
    sql5 = "INSERT INTO main_category(id, category) VALUES(5, 'High Vortex Large (aircraft such as B-757)')"
    sql6 = "INSERT INTO main_category(id, category) VALUES(6, 'Heavy (> 300000 lbs)')"
    sql7 = "INSERT INTO main_category(id, category) VALUES(7, 'High Performance (> 5g acceleration and 400 kts)')"
    sql8 = "INSERT INTO main_category(id, category) VALUES(8, 'Rotorcraft')"
    sql9 = "INSERT INTO main_category(id, category) VALUES(9, 'Glider / sailplane')"
    sql10 = "INSERT INTO main_category(id, category) VALUES(10, 'Lighter-than-air')"
    sql11 = "INSERT INTO main_category(id, category) VALUES(11, 'Parachutist / Skydiver')"
    sql12 = "INSERT INTO main_category(id, category) VALUES(12, 'Ultralight / hang-glider / paraglider')"
    sql13 = "INSERT INTO main_category(id, category) VALUES(13, 'Reserved')"
    sql14 = "INSERT INTO main_category(id, category) VALUES(14, 'Unmanned Aerial Vehicle')"
    sql15 = "INSERT INTO main_category(id, category) VALUES(15, ' Space / Trans-atmospheric vehicle')"
    sql16 = "INSERT INTO main_category(id, category) VALUES(16, 'Surface Vehicle – Emergency Vehicle')"
    sql17 = "INSERT INTO main_category(id, category) VALUES(17, 'Surface Vehicle – Service Vehicle')"
    sql18 = "INSERT INTO main_category(id, category) VALUES(18, 'Point Obstacle (includes tethered balloons)')"
    sql19 = "INSERT INTO main_category(id, category) VALUES(19, 'Cluster Obstacle')"
    sql20 = "INSERT INTO main_category(id, category) VALUES(20, 'Line Obstacle')"
    sql21 = "INSERT INTO main_category(id, category) VALUES(21, 'No information at all')"

    mycursor.execute("ALTER TABLE main_position_source AUTO_INCREMENT=0")
    mycursor.execute(sql1)
    print(sql1)
    mycursor.execute(sql2)
    print(sql2)
    mycursor.execute(sql3)
    print(sql3)
    mycursor.execute(sql4)
    print(sql4)
    mycursor.execute(sql5)
    print(sql5)
    mycursor.execute(sql6)
    print(sql6)
    mycursor.execute(sql7)
    print(sql7)
    mycursor.execute(sql8)
    print(sql8)
    mycursor.execute(sql9)
    print(sql9)
    mycursor.execute(sql10)
    print(sql10)
    mycursor.execute(sql11)
    print(sql11)
    mycursor.execute(sql12)
    print(sql12)
    mycursor.execute(sql13)
    print(sql13)
    mycursor.execute(sql14)
    print(sql14)
    mycursor.execute(sql15)
    print(sql15)
    mycursor.execute(sql16)
    print(sql16)
    mycursor.execute(sql17)
    print(sql17)
    mycursor.execute(sql18)
    print(sql18)
    mycursor.execute(sql19)
    print(sql19)
    mycursor.execute(sql20)
    print(sql20)
    mycursor.execute(sql21)
    print(sql21)

    db_con.commit()
    print('Category table has been populated with 21 records.')
    

def update_states_db(api_con, db_con):
    states = api_con.get_states()
    mycursor = db_con.cursor()
    mycursor.execute("USE open_sky_db_2022")
    n = 0
    for s in states.states:
        print(s)
        if s.position_source != 0:
            ps_id = s.position_source
        else:
            ps_id = 4
##        if s.category != 0:
##            cat = s.category
##        else:
        cat_id = 21
#        if n==20:
#            break
        
        sql_new_record_1 = '''INSERT INTO main_state(
            id,
            icao24,
            callsign,
            origin_country,
            time_position,
            last_contact,
            longitude,
            latitude,
            geo_altitude,
            on_ground, 
            velocity,
            true_track,
            vertical_rate,
            sensors,
            baro_altitude,
            squawk,
            spi,
            position_source_id,
            category_id)
            VALUES(NULL,'''
        sql1 = "'"+for_v(s.icao24)+"', '"+for_v(s.callsign)+"', '"+for_v(s.origin_country)+"', "
        sql2 = "'"+for_v(s.time_position)+"', '"+for_v(s.last_contact)+"', '"+for_v(s.longitude)+"', "
        sql3 = "'"+for_v(s.latitude)+"', '"+for_v(s.geo_altitude)+"', '"+for_v(s.on_ground)+"', "
        sql4 = "'"+for_v(s.velocity)+"', '"+for_v(s.true_track)+"', '"+for_v(s.vertical_rate)+"', " 
        sql5 = "'"+for_v(s.sensors)+"', '"+for_v(s.baro_altitude)+"', '"+for_v(s.squawk)+"', "
        sql6 = "'"+for_v(s.spi)+"', '"+for_v(ps_id)+"', "+for_v(cat_id)+")"
        sql_new_record_2 = sql1 + sql2 + sql3 + sql4 + sql5 + sql6

#        print(sql_new_record_1+sql_new_record_2)
        mycursor.execute(sql_new_record_1+sql_new_record_2)
        n += 1
    print()


    db_con.commit()
    LAST_DB_UPDATE_TIME = time.time()
    print('Total records: ' + str(n))
#    print(str(mycursor.rowcount()))
    print('The database is updated at ' + str(time.ctime(time.time())) + '.')

def plot_velocity_at_geo_alt(db_con, db, min_alt, max_alt):
    mycursor = db_con.cursor()
    mycursor.execute("USE " + db)
    mycursor.execute('SELECT velocity, geo_altitude FROM main_state WHERE geo_altitude > 0 AND geo_altitude <= '+str(max_alt) + ' ORDER BY geo_altitude ASC')
    speed_lst = []
    geo_alt_lst = []
    n = 0
    for row in mycursor.fetchall():
        speed_lst.append(row[0])
        geo_alt_lst.append(row[1])
    fig, ax = pplt.subplots()
    ax.plot(geo_alt_lst, speed_lst)
    pplt.show()


#print("Matthias Schäfer, Martin Strohmeier, Vincent Lenders, Ivan Martinovic and Matthias Wilhelm. Bringing Up OpenSky: A Large-scale ADS-B Sensor Network for Research. In Proceedings of the 13th IEEE/ACM International Symposium on Information Processing in Sensor Networks (IPSN), pages 83-94, April 2014.")
