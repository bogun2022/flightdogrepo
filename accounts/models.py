from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    user_ip = models.CharField(max_length = 30)
    user_icao24 = models.CharField(max_length = 10)
    user_origin_country = models.CharField(max_length = 30)
    user_longitude_min = models.DecimalField(max_digits = 7, decimal_places = 4, null = True)
    user_longitude_max = models.DecimalField(max_digits = 7, decimal_places = 4, null = True)    
    user_latitude_min = models.DecimalField(max_digits = 7, decimal_places = 4, null = True)
    user_latitude_max = models.DecimalField(max_digits = 7, decimal_places = 4, null = True)    
    user_geo_altitude_min = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)
    user_geo_altitude_max = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)
    user_baro_altitude_min = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)
    user_baro_altitude_max = models.DecimalField(max_digits = 7, decimal_places = 2, null = True)    
    user_category = models.CharField(max_length = 30)
