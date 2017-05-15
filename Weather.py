import requests, re, json

result_ip = requests.get('http://ipinfo.io')

#finds zipcode
ip_json_data = json.loads(result_ip.text)
ip_zipcode = ip_json_data['postal']


url = 'http://api.wunderground.com/api/214e2411900fbb2b/conditions/forecast/q/'+ip_zipcode+'.json'

result_forecast = requests.get(url)

json_data = json.loads(result_forecast.text)


#creates variables for all weather info
city = json_data['current_observation']['display_location']['full']
weather_zipcode = json_data['current_observation']['display_location']['zip']
current_temp = json_data['current_observation']['temperature_string']
feels_like= json_data['current_observation']['feelslike_string']
high_f = json_data['forecast']['simpleforecast']['forecastday'][0]['high']['fahrenheit']
high_c = json_data['forecast']['simpleforecast']['forecastday'][0]['high']['celsius']
low_f = json_data['forecast']['simpleforecast']['forecastday'][0]['low']['fahrenheit']
low_c = json_data['forecast']['simpleforecast']['forecastday'][0]['low']['celsius']
uv= json_data['current_observation']['UV']
humidity = json_data['current_observation']['relative_humidity']
precipitation = json_data['current_observation']['precip_today_string'] 
wind_direction = json_data['current_observation']['wind_dir']
wind_string = json_data['current_observation']['wind_string']
wind_speed = json_data['current_observation']['wind_mph']

#displays all info
print('City:', city, weather_zipcode)
print('Current Temperature:', current_temp)
print('Feels Like:', feels_like)
print('Today\'s High: %s F (%s C)' % (high_f, high_c))
print('Today\'s Low: %s F (%s C)' % (low_f, low_c))
print('UV Index:', uv)
print('Humidity:', humidity)
print('Precipitation Today:', precipitation)
print('Wind: %s mph %s. %s' % (wind_speed, wind_direction, wind_string))
