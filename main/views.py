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

# Create your views here.

def filter_attr(icao24,callsign,origin_country,lo_min,lo_max,la_min,la_max,ba_min,ba_max,ga_min,ga_max):
    arg_dict = {}

    if icao24 != '':
        arg_dict['icao24'] = icao24
    if callsign != '':
        arg_dict['callsign'] = callsign
    if origin_country != '':
        arg_dict['origin_country'] = origin_country

    arg_dict['longitude__range'] = (lo_min, lo_max)
    arg_dict['latitude__range'] = (la_min, la_max)

    arg_dict['baro_altitude__range'] = (ba_min, ba_max)
    arg_dict['geo_altitude__range'] = (ga_min, ga_max)
    
    return arg_dict


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
            
            txt = filter_attr(icao24,callsign,origin_country,longitude_min, longitude_max, latitude_min, latitude_max, baro_altitude_min,baro_altitude_max,geo_altitude_min,geo_altitude_max)
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
#               'txt':txt,
               'user':user,
               'states':states,
              }
      
#    return HttpResponse(template.render(context, request))
    return render(request, 'main/index.html', context)


def details(request, state_id):
    state = get_object_or_404(State, pk = state_id)
    return render(request, 'main/details.html', {'state':state})

def stat(request):
    user = request.user
    states = State.objects.order_by('time_position')
    template = loader.get_template('main/stat.html')
    if request.method == 'POST':
        filter_form = StateFilterForm(request.POST)
        stat_fields_form = StatFieldsForm(request.POST)
        charts_form = ChartsForm(request.POST)
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
            
            txt = filter_attr(icao24,callsign,origin_country,longitude_min, longitude_max, latitude_min, latitude_max, baro_altitude_min,baro_altitude_max,geo_altitude_min,geo_altitude_max)
            if txt != '':
                states = State.objects.filter(**txt).order_by('geo_altitude')
            else:
                states = ""
            
            speed_lst = []
            geo_alt_lst = []
            for state in states:
                speed_lst.append(state.velocity)
                geo_alt_lst.append(state.geo_altitude)

            parameter1 = ""
            parameter2 = ""
            url = statfun.chart_by_par(states, parameter1, parameter2, date_from, date_to)

#            return HttpResponseRedirect('/stat/')
    else:
        txt = ''
        filter_form = StateFilterForm()
        stat_fields_form = StatFieldsForm()
        charts_form = ChartsForm()
        url = ""
        geo_alt_lst = 0
        speed_lst = 0        
                       
    context = {
               'filter_form':filter_form,
               'stat_fields_form':stat_fields_form,
               'charts_form':charts_form,
#               'txt':txt,
               'user':user,
               'states':states,
               'data':url,
               'geo_alt_lst':geo_alt_lst,
               'speed_lst':speed_lst,               
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

