from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import CustomUserCreationForm
from accounts.forms import CustomUserChangeForm
from django.contrib.auth.models import User
from accounts.models import CustomUser

class RegisterForm(CustomUserCreationForm):
    email = forms.EmailField(required = True)

    class Meta():
        model = CustomUser
        fields = ["username","email","password1","password2"]

class StateFilterForm(forms.Form):
    icao24 = forms.CharField(label = 'ICAO24', max_length = 6, required = False)
    callsign = forms.CharField(label = 'Callsign', max_length = 7, required = False)
#    origin_country = forms.CharField(label = 'Origin country', initial = CustomUser.user_origin_country, max_length = 30, required = False)
    origin_country = forms.CharField(label = 'Origin country', max_length = 30, required = False)
    
    longitude_min = forms.DecimalField(label = 'Longitude min', max_digits = 7, decimal_places = 4, required = True, initial = 0)
    longitude_max = forms.DecimalField(label = 'Longitude max', max_digits = 7, decimal_places = 4, required = True, initial = 180)
    latitude_min = forms.DecimalField(label = 'Latitude min', max_digits = 7, decimal_places = 4, required = True, initial = 0)
    latitude_max = forms.DecimalField(label = 'Latitude max', max_digits = 7, decimal_places = 4, required = True, initial = 90)

    baro_altitude_min = forms.DecimalField(label = 'Min baro altitude', max_digits = 7, decimal_places = 2, required = True, initial = 0)
    baro_altitude_max = forms.DecimalField(label = 'Max baro altitude', max_digits = 7, decimal_places = 2, required = True, initial = 15000)

    geo_altitude_min = forms.DecimalField(label = 'Min geo altitude',  max_digits = 7, decimal_places = 2, required = True, initial = 0)
    geo_altitude_max = forms.DecimalField(label = 'Max geo altitude',  max_digits = 7, decimal_places = 2, required = True, initial = 15000)

#    on_ground = forms.CharField(label = 'On ground', max_length = 5, required = False)

#    spi = forms.CharField(label = ' max_length = 5, required = False)
#    position_source = forms.ForeignKey(label = 'Position source', Position_source, on_delete = models.CASCADE, required = False)
#    category = forms.ForeignKey(label = 'Category', Category, on_delete = models.CASCADE, required = False)


class StatForm(forms.Form):
    date_from = forms.DateField(label = 'From:')
    date_to = forms.DateField(label = 'to')
