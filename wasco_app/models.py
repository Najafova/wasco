from django.db import models

# Create your models here.

class DeviceData(models.Model):
    id = models.AutoField(primary_key=True)
    dev_id = models.CharField(max_length=255)
    battery = models.FloatField(blank=True, null=True)
    bin_state = models.IntegerField(blank=True, null=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return "{} {} {}".format(self.dev_id, self.battery, self.bin_state)

    class Meta:
        verbose_name = "Device data"
        verbose_name_plural = "Device data"
        ordering = ['order',]

    def device_icon(self):
        if self.bin_state>=0 and self.bin_state<25:
            return "/static/wasco/images/green.png"
        elif self.bin_state>=25 and self.bin_state<50:
            return "/static/wasco/images/yellow.png"
        elif self.bin_state>=50 and self.bin_state<75:
            return "/static/wasco/images/orange.png"
        elif self.bin_state>=75:
            return "/static/wasco/images/red.png"

    
    def default(self):
        if self.bin_state>=0 and self.bin_state<25:
            return "/static/wasco/images/green.png"


class DeviceSettings(models.Model):
    id = models.AutoField(primary_key=True)
    dev_id = models.CharField(max_length=255)
    bin_height = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True) 
    longitude = models.FloatField(blank=True, null=True) 

    def __str__(self):
        return "{} {} {} {}".format(self.dev_id, self.longitude, self.latitude, self.bin_height)

    class Meta:
        verbose_name = "Device location"
        verbose_name_plural = "Device location"



class LogData(models.Model):
    dev_id = models.CharField(max_length=255)    
    battery = models.FloatField(blank=True, null=True)
    bin_state = models.IntegerField(blank=True, null=True)
    request_time = models.CharField(max_length=255)

    def __str__(self):
        return "{} {} {} {}".format(self.dev_id, self.battery, self.bin_state, self.request_time)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"