from django.db import models
import time

# Create your models here.
class Position_source(models.Model):
    position_source = models.CharField(max_length = 10)
    def __str__(self):
#        return self.position_source + " (" + str(self.id) + ")"
        return self.position_source

class Category(models.Model):
    category = models.CharField(max_length = 60)
    def __str__(self):
#        return self.category + " (" + str(self.id) + ")"
        return self.category
    
class State(models.Model):
    icao24 = models.CharField(max_length = 10)
    callsign = models.CharField(max_length = 10)
    origin_country = models.CharField(max_length = 30)
    time_position = models.IntegerField(default = 0)
    last_contact = models.IntegerField(default = 0)
    longitude = models.DecimalField(max_digits = 7, decimal_places = 4)
    latitude = models.DecimalField(max_digits = 7, decimal_places = 4)
    geo_altitude = models.DecimalField(max_digits = 7, decimal_places = 2)
    on_ground = models.CharField(max_length = 5)
    velocity = models.DecimalField(max_digits = 7, decimal_places = 2)
    true_track = models.DecimalField(max_digits = 5, decimal_places = 2)
    vertical_rate = models.DecimalField(max_digits = 5, decimal_places = 2)
    sensors = models.CharField(max_length = 15)
    baro_altitude = models.DecimalField(max_digits = 7, decimal_places = 2)
    squawk = models.IntegerField(default = 0)
    spi = models.CharField(max_length = 5)
    position_source = models.ForeignKey(Position_source, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    db_update_num = models.IntegerField(default = 0)

    def __str__(self):
        str_aircraft = "Aircraft icao24: "+self.icao24+" callsign: "+self.callsign\
                       +" from: "+self.origin_country+" at "+str(time.ctime(self.time_position))\
                       +" last contact at "+str(time.ctime(self.last_contact))
        str_position = " longitude: "+str(self.longitude)+" latitude: "+str(self.latitude)\
                        +" geo altitude: "+str(self.geo_altitude)+" velocity: "+str(self.velocity)\
                        +" true track: "+str(self.true_track)+ " vertical rate: "+str(self.vertical_rate)\
                        +" sensors: "+str(self.sensors)+" baroaltitude: "+str(self.baro_altitude)\
                        +" squawk code: "+str(self.squawk) + " position source: "+str(self.position_source)+" aircraft category: "+str(self.category)

        if self.spi == "True":
            str_spi = " on special purpose "
        else:
            str_spi = ""

        if self.position_source == 0:
            str_ps = " position source: ADS-B"
        elif self.position_source == 1:
            str_ps = " position source: ASTERIX"
        elif self.position_source == 2:
            str_ps = " position source: MLAT"
        elif self.position_source == 3:
            str_ps = " position source: FLARM"
        else:
            str_ps = ""
        
        if self.on_ground == "True":
            full_str = str_aircraft + " - current status: on ground"
        else:
            full_str = str_aircraft + str_position + str_spi + str_ps

        return full_str


class Global_param():
        db_update_frequence = models.IntegerField(default = 3600)
        last_db_update = models.IntegerField(default = 0)
