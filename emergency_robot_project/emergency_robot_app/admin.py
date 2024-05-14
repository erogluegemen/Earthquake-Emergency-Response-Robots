from django.contrib import admin
from .models import *

admin.site.register(EarthquakeVictim)
admin.site.register(CameraSensorData)
admin.site.register(PIRSensorData)
admin.site.register(Picture)