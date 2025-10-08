import requests
import datetime as dt
import gtts
import pygame

def kelvin_to_celsius_fahrenheit(kelvin):
    celcius = kelvin - 273.15
    fahrenheit = celcius * (9/5) + 32
    return celcius, fahrenheit


# lat and lon is kediri coordinate
lat = -7.8111057
lon = 112.0046051
api_key = "e56f335aa287e580bceb37a61532557e"
city = "Kediri"

# main program to request weather API
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
response = requests.get(url).json()



# Information we get
temp_kelvin = response['main']['temp']
temp_celcius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
feels_like_kelvin = response['main']['feels_like']
feels_like_celcius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
humidity = response['main']['humidity']
wind_speed = response['wind']['speed']
description = response['weather'][0]['description']
sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])



text = f"Sure, Here's the Current Weather Information    .The Temperature is {temp_celcius:.2f}°Celcius or {temp_fahrenheit:.2f}°Fahrenheit , The Humidity is {humidity}%, The Temperature Feels Like is {feels_like_celcius:.2f}°Celsius or {feels_like_fahrenheit:.2f}°Fahrenheit, The average Wind Speed is {wind_speed}m/s, and the General Weather is {description}, Sun rises at = {sunrise_time} local time ,Sun sets at = {sunset_time} local time"
speech = gtts.gTTS(text)
name_file = ("Weather_info.mp3")
speech.save(name_file)

pygame.mixer.init()
pygame.mixer.music.load(name_file)
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(1000)
