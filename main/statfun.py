import pymysql
import time
import datetime

import matplotlib.pyplot as plt
import io
import urllib, base64
import statistics as st
from django.db.models import Sum

def filter_attr(icao24,callsign,origin_country,date_from,date_to,lo_min,lo_max,la_min,la_max,ba_min,ba_max,ga_min,ga_max):
    arg_dict = {}
    if icao24 != '':
        arg_dict['icao24'] = icao24
    if callsign != '':
        arg_dict['callsign'] = callsign
    if origin_country != '':
        arg_dict['origin_country'] = origin_country
    arg_dict['time_position__range'] = origin_country
    arg_dict['longitude__range'] = (lo_min, lo_max)
    arg_dict['latitude__range'] = (la_min, la_max)
    arg_dict['baro_altitude__range'] = (ba_min, ba_max)
    arg_dict['geo_altitude__range'] = (ga_min, ga_max)
    arg_dict['time_position__range'] = (int(date_from), int(date_to))
    return arg_dict

def filter_attr_txt(icao24,callsign,origin_country,date_from,date_to,lo_min,lo_max,la_min,la_max,ba_min,ba_max,ga_min,ga_max):
    arg_txt = ""

    if icao24 != '':
        arg_txt += "icao24 = "+str(icao24)
        arg_txt += ","        
    if callsign != '':
        arg_txt += "callsign = "+str(callsign)
        arg_txt += ","
    if origin_country != '':
        arg_txt += "origin_country = "+str(origin_country)
        arg_txt += ","
        
        arg_txt += "time_position__range = "+str(time_position__range)
        arg_txt += ","        

        arg_txt += "longitude__range = "+str(longitude__range)
        arg_txt += ","        
        arg_txt += "latitude__range = "+str(latitude__range)
        arg_txt += ","

        arg_txt += "baro_altitude__range = "+str((ba_min, ba_max))
        arg_txt += ","        
        arg_txt += "geo_altitude__range = "+str((ga_min, ga_max))
        arg_txt += ","
        
        arg_txt += "time_position__range = "+str(time_position__range)

    return arg_txt


def get_ranges(par_min, par_max, step):
    if par_min >= par_max:
        return None
    if step > par_max:
        return None
    if par_max == 0 or step == 0:
        return None
    
    total_range = par_max - par_min
    ranges_list = []
    if total_range > step:
        num = int(total_range // step)
        fraction = total_range % step
        for n in range(num):
            ranges_list.append([par_min, par_min + step])
            par_min += step
        if par_max - par_min > 0:
            ranges_list.append([par_min, par_max])
    else:
        ranges_list = [[par_min, par_max]]
    return ranges_list

def last_step(par_min, par_max, step):
    n = iter_num(par_min, par_max, step)
    if n != 1:
        fraction = par_max % step
    elif par_max < step:
        print()
        
def chart_by_par(tab, par1, par2, date_from, date_to):
##    speed_lst = []
##    geo_alt_lst = []
##    for state in tab:
##        speed_lst.append(state.velocity)
##        geo_alt_lst.append(state.geo_altitude)
    plt.plot(par1, par2)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format = 'png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    url = urllib.parse.quote(string)
#    url.show()
    return url
  
def average_cong_by_alt(tab, alt_min, alt_max, step, date_from, date_to):
    stat_data = ""
    total_airplanes = 0
    ranges = get_ranges(alt_min, alt_max, step)
    for n in ranges:
        a_min = n[0]
        a_max = n[1]
        states = tab.filter(geo_altitude__range = ((a_min, a_max)))
        airplanes = states.all().count()
        total_airplanes += airplanes
        stat_data += "Geo_altitude from " + str(a_min) + "m to " + str(a_max) + "m: average congestion is: " + str(airplanes) + " aircraft carriers "
    stat_data += " Total aircraft: " + str(total_airplanes)
    return stat_data

def average_cong_by_dt(tab, dt_from, dt_to, step, date_from, date_to):
    stat_data = ""
    total_airplanes = 0
    ranges = get_ranges(dt_from, dt_to, step)
    for n in ranges:
        time_from = n[0]
        time_to = n[1]
        states = tab.filter(time_position__range = ((time_from, time_to)))
        airplanes = states.all().count()
        total_airplanes += airplanes
        tf = datetime.datetime.fromtimestamp(time_from).strftime("%A, %B %d, %Y %I:%M:%S")
        tt = datetime.datetime.fromtimestamp(time_to).strftime("%A, %B %d, %Y %I:%M:%S")
#        stat_data += "Time from " + str(tf) + " to " + str(tt) + ": average congestion is: " + str(airplanes) + " aircraft carriers "
        stat_data += " " + str(airplanes) + " aircraft carriers "
    stat_data += " Total aircraft: " + str(total_airplanes)
    return stat_data


def average_vel_by_alt(tab, alt_min, alt_max, step, date_from, date_to):
    stat_data = ""
    ranges = get_ranges(alt_min, alt_max, step)
    for n in ranges:
        a_min = n[0]
        a_max = n[1]
        states = tab.filter(geo_altitude__range = ((a_min, a_max)))
        vel_lst = []
        for state in states:
            vel_lst.append(state.velocity)
        if vel_lst != []:
            average = round(st.mean(vel_lst),2)
        else:
            average = 0
        stat_data += "Geo_altitude from " + str(a_min) + "m to " + str(a_max) + "m: average velocity is: " + str(average) + "m/s "
    return stat_data

def average_vertrate_by_alt(tab, alt_min, alt_max, step, date_from, date_to):
    stat_data = ""
    ranges = get_ranges(alt_min, alt_max, step)
    for n in ranges:
        a_min = n[0]
        a_max = n[1]
        states = tab.filter(geo_altitude__range = ((a_min, a_max)))
        vel_lst = []
        for state in states:
            vel_lst.append(state.vertical_rate)
        if vel_lst != []:
            average = round(st.mean(vel_lst),2)
        else:
            average = 0
        stat_data += "Geo_altitude from " + str(a_min) + "m to " + str(a_max) + "m: average vertical rate is: " + str(average) + "m/s "
    return stat_data

def aircraft_by_countries(tab, date_from, date_to):
    lst = []
    stat_data = ""
    cur_country = ""
    cur_countries = 0
    total_countries = 0
    states = tab.order_by('origin_country')
    for state in states:
        if cur_countries == 0:
            cur_country = state.origin_country
            cur_countries += 1
            stat_data += str(cur_country) + ": "
        elif state.origin_country == cur_country:
            cur_countries += 1
        else:
            stat_data += str(int(cur_countries)) + " "
            cur_country = state.origin_country
            stat_data += str(cur_country) + ": "
            cur_countries = 1
        total_countries += 1
    stat_data += " Total countries: " + str(int(total_countries))
    return stat_data                              



def main():
    a = 3
    b = 4
    c = 5
    d = [a,b,c]
    e = st.mean(d)
    print("Mean value is:")
    print(e)

d = datetime.datetime.fromtimestamp(1659775829).strftime('%Y-%m-%d %H:%M:%S')
print(d)

e = get_ranges (34.5, 178.6, 23)
print(e)
