from SECRETS import APIKEY
from requests import get



def get_current_weather(latlng):
	API_URL = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={key}&units=imperial'.format(lat=latlng[0], lng=latlng[1], key=APIKEY)
	weather_data = get(API_URL).json()
	return weather_data

if __name__ == '__main__':
	print(get_current_weather([40.412, -86.937]))
