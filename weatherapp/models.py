from django.db import models
from django.contrib.auth.models import User


from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accuweather_api_key = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user)


class WeatherSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    search_date = models.DateTimeField(auto_now_add=True)
    weather_data = models.JSONField(null=True, blank=True) 

    def __str__(self):
        return str(self.location)