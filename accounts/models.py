from django.db import models
import datetime

# Create your models here.

# HOST MODEL
class Host(models.Model):
    id = models.AutoField
    host_name = models.CharField(max_length=50)
    host_email = models.EmailField(blank=True, null=True)
    host_phone = models.IntegerField(max_length=10)
    host_image = models.ImageField(upload_to='img/doctors')
    host_desc = models.CharField(max_length=50)
    address = models.CharField(max_length=100,default="HealthPlus, Rohini-22, New Delhi")
    status = models.BooleanField(default=True)
    available = models.CharField(max_length=50,default='')
    current_meeting_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + " : " + str(self.host_name)

# MEETING MODEL
class Meeting(models.Model):
    id = models.AutoField
    visitor_name = models.CharField(max_length=50)
    visitor_email = models.EmailField(blank=True, null=True)
    visitor_phone = models.IntegerField(max_length=10)
    host = models.CharField(max_length=50, default="")
    date = models.DateField(default=datetime.datetime.now())
    time_in = models.TimeField(default=datetime.datetime.now())
    time_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)+ ' : ' + str(self.visitor_name)

