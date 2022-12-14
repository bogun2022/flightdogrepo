from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import State
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages

from .forms import RegisterForm, StateFilterForm, StatFieldsForm, ChartsForm
from django.contrib.auth import login, logout, authenticate

from ipware import get_client_ip
import matplotlib.pyplot as plt
from . import osdb, statfun
import io
import urllib, base64
import statistics as st
import datetime

# Create your views here.


def index(request):
    user = request.user
    states = State.objects.order_by('time_position')
    template = loader.get_template('main/index.html')
    if user.is_authenticated == True:
        init_data = {
            'icao24':user.user_icao24,
            'origin_country':user.user_origin_country,
            'baro_altitude_min':user.user_baro_altitude_min,
            'baro_altitude_max':user.user_baro_altitude_max,
            'geo_altitude_min':user.user_geo_altitude_min,
            'geo_altitude_max':user.user_geo_altitude_max,
            'longitude_min':user.user_longitude_min,
            'longitude_max':user.user_longitude_max,
            'latitude_min':user.user_latitude_min,
            'latitude_max':user.user_latitude_max,
            }

    if request.method == 'POST':
        filter_form = StateFilterForm(request.POST, initial = init_data)
        if filter_form.is_valid():
            icao24 = filter_form.cleaned_data['icao24']
            callsign = filter_form.cleaned_data['callsign']
            origin_country = filter_form.cleaned_data['origin_country']
            baro_altitude_min = filter_form.cleaned_data['baro_altitude_min']
            baro_altitude_max = filter_form.cleaned_data['baro_altitude_max']
            geo_altitude_min = filter_form.cleaned_data['geo_altitude_min']
            geo_altitude_max = filter_form.cleaned_data['geo_altitude_max']
            longitude_min = filter_form.cleaned_data['longitude_min']
            longitude_max = filter_form.cleaned_data['longitude_max']
            latitude_min = filter_form.cleaned_data['latitude_min']
            latitude_max = filter_form.cleaned_data['latitude_max']

            date_from = int(0)
            date_to = int(datetime.datetime.today().timestamp())
            
            txt = statfun.filter_attr(icao24,callsign,origin_country,0,date_to,longitude_min, longitude_max, latitude_min, latitude_max, baro_altitude_min,baro_altitude_max,geo_altitude_min,geo_altitude_max)
            if txt != '':
                states = State.objects.filter(**txt)
            if user.is_authenticated == True:
                # Save user preferences
                user.user_ip = get_client_ip(request)
                user.user_icao24 = filter_form.cleaned_data['icao24']
                user.user_origin_country = filter_form.cleaned_data['origin_country']
                user.user_longitude_min = filter_form.cleaned_data['longitude_min']
                user.user_longitude_max = filter_form.cleaned_data['longitude_max']    
                user.user_latitude_min = filter_form.cleaned_data['latitude_min']
                user.user_latitude_max = filter_form.cleaned_data['latitude_max']    
                user.user_geo_altitude_min = filter_form.cleaned_data['geo_altitude_min']
                user.user_geo_altitude_max = filter_form.cleaned_data['geo_altitude_max']
                user.user_baro_altitude_min = filter_form.cleaned_data['baro_altitude_min']
                user.user_baro_altitude_max = filter_form.cleaned_data['baro_altitude_max']    
#              user.user_category = filter_form.cleaned_data['category']
                user.save()

#            return HttpResponseRedirect('/index/')
    else:
        txt = ''
        if user.is_authenticated == True:
            init_data = {
                'icao24':user.user_icao24,
                'origin_country':user.user_origin_country,
                'baro_altitude_min':user.user_baro_altitude_min,
                'baro_altitude_max':user.user_baro_altitude_max,
                'geo_altitude_min':user.user_geo_altitude_min,
                'geo_altitude_max':user.user_geo_altitude_max,
                'longitude_min':user.user_longitude_min,
                'longitude_max':user.user_longitude_max,
                'latitude_min':user.user_latitude_min,
                'latitude_max':user.user_latitude_max,
                }
            filter_form = StateFilterForm(initial = init_data)
        else:
            filter_form = StateFilterForm()
        

#        return render (request, 'main/index.html', {'form':form})

    context = {
               'filter_form':filter_form,
               'user':user,
               'states':states,
              }
      
#    return HttpResponse(template.render(context, request))
    return render(request, 'main/index.html', context)


def details(request, state_id):
    state = get_object_or_404(State, pk = state_id)
    return render(request, 'main/details.html', {'state':state})

def stat(request):
    par = ""
    chart_data = ""
    parameter1 = ""
    parameter2 = ""
    data = ""

    user = request.user
    states = State.objects.order_by('time_position')
    template = loader.get_template('main/stat.html')
    if request.method == 'POST':
        filter_form = StateFilterForm(request.POST)
        stat_fields_form = StatFieldsForm(request.POST)
        charts_form = ChartsForm(request.POST)

        if filter_form.is_valid() and stat_fields_form.is_valid():
            icao24 = filter_form.cleaned_data['icao24']
            callsign = filter_form.cleaned_data['callsign']
            origin_country = filter_form.cleaned_data['origin_country']
            baro_altitude_min = filter_form.cleaned_data['baro_altitude_min']
            baro_altitude_max = filter_form.cleaned_data['baro_altitude_max']
            geo_altitude_min = filter_form.cleaned_data['geo_altitude_min']
            geo_altitude_max = filter_form.cleaned_data['geo_altitude_max']
            longitude_min = filter_form.cleaned_data['longitude_min']
            longitude_max = filter_form.cleaned_data['longitude_max']
            latitude_min = filter_form.cleaned_data['latitude_min']
            latitude_max = filter_form.cleaned_data['latitude_max']

            date_from = stat_fields_form.cleaned_data['date_from']
            date_to = stat_fields_form.cleaned_data['date_to']
            date_from = int(datetime.datetime.combine(date_from, datetime.time()).timestamp())
            date_to = int(datetime.datetime.combine(date_to, datetime.time()).timestamp())

            txt = statfun.filter_attr(icao24,callsign,origin_country,date_from,date_to,longitude_min, longitude_max, latitude_min, latitude_max, baro_altitude_min,baro_altitude_max,geo_altitude_min,geo_altitude_max)
#            states = State.objects.filter(**txt).order_by('geo_altitude')
            states = State.objects.filter(**txt)               

            vel_lst = []
            vert_rate_lst = []
            geo_alt_lst = []
            for state in states:
                vel_lst.append(state.velocity)
                vert_rate_lst.append(state.vertical_rate)
                geo_alt_lst.append(state.geo_altitude)
            par = vel_lst
            stat_opt = request.POST.get("select_stat_option")
#            stat_data = statfun.get_average_calc(stat_opt)
            if stat_opt == "average_cong_by_alt":
                stat_data = statfun.average_cong_by_alt(states, geo_altitude_min, geo_altitude_max, 1000, date_from, date_to)
#                chart_data = statfun.chart_by_par(states, parameter1, parameter2, date_from, date_to)
            elif stat_opt == "average_cong_by_dt":
                stat_data = statfun.average_cong_by_dt(states, date_from, date_to, 3600, date_from, date_to)
#                chart_data = statfun.chart_by_par(states, parameter1, parameter2, date_from, date_to)
            elif stat_opt == "average_vel_by_alt":
                stat_data = statfun.average_vel_by_alt(states, geo_altitude_min, geo_altitude_max, 1000, date_from, date_to)
                chart_data = statfun.chart_by_par(states, geo_alt_lst, vel_lst, date_from, date_to)
            elif stat_opt == "average_vertrate_by_alt":
                stat_data = statfun.average_vertrate_by_alt(states, geo_altitude_min, geo_altitude_max, 1000, date_from, date_to)
                chart_data = statfun.chart_by_par(states, geo_alt_lst, vert_rate_lst, date_from, date_to)
            elif stat_opt == "countries_airborn_ratio":
                stat_data = statfun.aircraft_by_countries(states, date_from, date_to)
#                chart_data = statfun.chart_by_par(states, parameter1, parameter2, date_from, date_to)
            else:
                stat_data = "Not selected"
                chart_data = "not provided"

#            if stat_opt == "average_cong_by_alt":
#            else:
#                url = statfun.chart_vel_by_alt(states, parameter1, parameter2, date_from, date_to)
                
#            return HttpResponseRedirect('/stat/')
    else:
        par = ""
        txt = ''
        filter_form = StateFilterForm()
        stat_fields_form = StatFieldsForm()
        charts_form = ChartsForm()
        chart_data = ""
        data = ""
        geo_alt_lst = 0
        vel_lst = 0
        vert_rate_lst = 0        
        stat_opt = ""
        stat_data = ""
        date_from = ""
        date_to = ""

    context = {
               'filter_form':filter_form,
               'stat_fields_form':stat_fields_form,
               'charts_form':charts_form,
               'user':user,
               'states':states,
               'geo_alt_lst':geo_alt_lst,
               'vel_lst':vel_lst,
               'vert_rate_lst':vert_rate_lst,               
               'stat_data':stat_data,
               'data':chart_data,
               'txt':txt,
               'par':par,
               'vert_rate_lst':vert_rate_lst,
              }
    
#    return HttpResponse(template.render(context, request))
    return render(request, 'main/stat.html', context)    


def home(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})

    return render(request, 'main/home.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
#            login(request, user)
            return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})

