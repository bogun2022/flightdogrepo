import pymysql
import time
import datetime

import matplotlib.pyplot as plt
import io
import urllib, base64
import statistics as st

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
        
        

def chart_vel_by_alt(tab, par1, par2, date_from, date_to):
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
  
def averave_cong_by_alt(tab, attr_lst, alt_min, alt_max, step, date_from, date_to):
    stat_data = ""
    total_airplanes = 0
    ranges = get_ranges(alt_min, alt_max, step)
    for n in ranges:
        a_min = n[0]
        a_max = n[1]
#        attr_lst[11] = a_min
#        attr_lst[12] = a_max
#        states = tab.objects.filter(**attr_lst)
#        states = tab.filter(**attr_lst)
        states = tab.filter(geo_altitude__range = ((a_min, a_max)))
        airplanes = states.all().count()
        total_airplanes += airplanes
        stat_data += "Geo_altitude from " + str(a_min) + "m to " + str(a_max) + "m: average congestion is: " + str(airplanes) + " aircraft carriers "
    stat_data += " Total aircraft: " + str(total_airplanes)
    return stat_data

        
        
##    speed_lst = []
##    geo_alt_lst = []
##    for state in tab:
##        speed_lst.append(state.velocity)
##        geo_alt_lst.append(state.geo_altitude)
##    plt.plot(geo_alt_lst, speed_lst)
##    fig = plt.gcf()
##    buf = io.BytesIO()
##    fig.savefig(buf, format = 'png')
##    buf.seek(0)
##    string = base64.b64encode(buf.read())
##    url = urllib.parse.quote(string)

    return url

def main():
    a = 3
    b = 4
    c = 5
    d = [a,b,c]
    e = st.mean(d)
    print("Mean value is:")
    print(e)

def main1():
    ranges = get_ranges(2000, 6500, 1000)
    for n in ranges:
        a_min = n[0]
        a_max = n[1]
        print (a_min," ", a_max)
        d = averave_cong_by_alt(tab, alt_min, alt_max, step, date_from, date_to)
        print

#main1()

d = datetime.datetime.fromtimestamp(1659775829).strftime('%Y-%m-%d %H:%M:%S')
print(d)

e = get_ranges (34.5, 178.6, 23)
print(e)
