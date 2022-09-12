from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import State
from django.contrib.auth import login
from django.contrib import messages

from .forms import RegisterForm, StateFilterForm
from django.contrib.auth import login, logout, authenticate

from ipware import get_client_ip

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
    ip, is_routable = get_client_ip(request)
    if ip is None:
        pass
    else:
        pass
        if is_routable:
            pass
        else:
            pass            

    states = State.objects.order_by('time_position')
    template = loader.get_template('main/index.html')
    if request.method == 'POST':
        form = StateFilterForm(request.POST)
        if form.is_valid():
            icao24 = form.cleaned_data['icao24']
            callsign = form.cleaned_data['callsign']
            origin_country = form.cleaned_data['origin_country']

            baro_altitude_min = form.cleaned_data['baro_altitude_min']
            baro_altitude_max = form.cleaned_data['baro_altitude_max']

            geo_altitude_min = form.cleaned_data['geo_altitude_min']
            geo_altitude_max = form.cleaned_data['geo_altitude_max']

            longitude_min = form.cleaned_data['longitude_min']
            longitude_max = form.cleaned_data['longitude_max']

            latitude_min = form.cleaned_data['latitude_min']
            latitude_max = form.cleaned_data['latitude_max']
            
            txt = filter_attr(icao24,callsign,origin_country,longitude_min, longitude_max, latitude_min, latitude_max, baro_altitude_min,baro_altitude_max,geo_altitude_min,geo_altitude_max)
            if txt != '':
                print()
                states = State.objects.filter(**txt)

            # Save user preferences
            user_ip = ip
            user_icao24 = form.cleaned_data['icao24']
            user_origin_country = form.cleaned_data['icao24']
            user_longitude_min = form.cleaned_data['longitude_min']
            user_longitude_max = form.cleaned_data['longitude_max']    
            user_latitude_min = form.cleaned_data['latitude_min']
            user_latitude_max = form.cleaned_data['latitude_max']    
            user_geo_altitude_min = form.cleaned_data['geo_altitude_min']
            user_geo_altitude_max = form.cleaned_data['geo_altitude_max']
            user_baro_altitude_min = form.cleaned_data['baro_altitude_min']
            user_baro_altitude_max = form.cleaned_data['baro_altitude_max']    
#            user_category = form.cleaned_data['category']
#            form.save()

#            return HttpResponseRedirect('/index/')
    else:
        txt = ''
        form = StateFilterForm()
#        return render (request, 'main/index.html', {'form':form})

    context = {
               'form':form,
#               'txt':txt,
               'ip':ip,
               'user':user,
               'states':states,
              }
      
#    return HttpResponse(template.render(context, request))
    return render(request, 'main/index.html', context)


def details(request, state_id):
    state = get_object_or_404(State, pk = state_id)
    return render(request, 'main/details.html', {'state':state})

def home(request):
    return render(request, 'main/home.html')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})

