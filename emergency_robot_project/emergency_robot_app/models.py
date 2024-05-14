from django.db import models

class EarthquakeVictim(models.Model):
    STATUS_CHOICES = [
        ('Dead', 'Dead'),
        ('No Injury', 'No Injury'),
        ('Minor Injury', 'Minor Injury'),
        ('Major Injury', 'Major Injury'),
    ]

    SOURCE_CHOICES = [
        ('Camera', 'Camera'),
        ('Microphone', 'Microphone'),
        ('PIR Sensor', 'PIR Sensor'),
    ]

    person_id = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='No Injury')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)

    def __str__(self):
        return f"Victim ID: {self.person_id}, Coordinates: ({self.x_coordinate}, {self.y_coordinate}), Status: {self.status}, Source: {self.source}"


class CameraSensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()

    def __str__(self):
        return f"Camera Sensor Data - {self.timestamp}"

class PIRSensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    motion_detected = models.BooleanField()

    def __str__(self):
        return f"PIR Sensor Data - {self.timestamp}"

    
class Picture(models.Model):
    image = models.ImageField(upload_to='captured_pictures/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Picture captured at {self.timestamp}'