import requests
from .models import UserProfile  

def get_weather_data(location_name, user, forecast_type='current'):
    try:
        user_profile = UserProfile.objects.get(user=user)
        api_key = user_profile.accuweather_api_key


        params = {
            'q': location_name,
            'apikey': api_key,
        }

        location_search_endpoint = 'http://dataservice.accuweather.com/locations/v1/cities/search'
        response = requests.get(location_search_endpoint, params=params)
        location_data = response.json()
        
        if location_data:
            location_key = location_data[0]['Key']

            if forecast_type == 'current':
                forecast_endpoint = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}'
            elif forecast_type == 'daily':
                forecast_endpoint = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}'
            else:
                return None

            forecast_response = requests.get(forecast_endpoint, params=params)
            forecast_data = forecast_response.json()
            return forecast_data
        else:
            return None
    except UserProfile.DoesNotExist:
        return None
