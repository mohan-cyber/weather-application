from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# import models
from .models import UserProfile, WeatherSearch

from .utils import get_weather_data



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        api_key = request.POST.get('api_key')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists. try different one'})


        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, accuweather_api_key=api_key)

        return redirect('login')

    return render(request, 'signup.html')

def is_not_authenticated(user):
    return not user.is_authenticated

# @user_passes_test(is_not_authenticated, login_url='search')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('search')  
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})

    return render(request, 'login.html')


def search(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        
        
        search_entry = WeatherSearch.objects.filter(user=request.user, location=location).first()
        
        if search_entry and search_entry.weather_data:
            weather_data = search_entry.weather_data
            
        else:
            weather_data = get_weather_data(location, request.user)
            if weather_data is not None:
                WeatherSearch.objects.create(user=request.user, location=location, weather_data=weather_data)
            else:
                return render(request, 'search.html', {'error': 'Weather data not available'})
        
        weather_data_dict = weather_data[0] if isinstance(weather_data, list) else weather_data

        return render(request, 'search.html', {'location': location, 'weather_data': weather_data_dict})

    return render(request, 'search.html')







