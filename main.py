from UnleashClient import UnleashClient
import requests
from flask import Flask, request

app = Flask(__name__)


client = UnleashClient(
    url='http://10.100.249.219:4242/api',
    app_name='my-python-app',
    custom_headers={
        'Authorization': 'default:development.unleash-insecure-api-token'
    }
)
client.initialize_client()


@app.route('/')
def hello_world():
    return '<h2>Laboratorio 9</h2>'


def get_lat_long_from_new(place):
    url = f'https://geocoding-api.open-meteo.com/v1/search?name={place}'
    r_coordinates = requests.get(url)
    jsonData = r_coordinates.json()
    return jsonData['results'][0]['latitude'], jsonData['results'][0]['longitude']


def get_lat_long_from_old(place):
    url = f'https://nominatim.openstreetmap.org/search?q={place}&format=json'
    r_coordinates = requests.get(url)
    jsonData = r_coordinates.json()
    return jsonData[0]['lat'], jsonData[0]['lon']


@app.route('/<place>')
def get_lat_lon(place):
    userId = request.args.get('userId')
    app_context = {'userId': userId}

    print("Usuario:", userId)

    if client.is_enabled('nuevoapi', app_context):
        print("Usando nuevo API")
        lat_res, lon_res = get_lat_long_from_new(place)
    else:
        print("Usando viejo API")
        lat_res, lon_res = get_lat_long_from_old(place)

    print("Latitud:", lat_res)
    print("Longitud:", lon_res)

    url_weather_daily = f'https://api.open-meteo.com/v1/forecast?latitude={lat_res}&longitude={lon_res}&forecast_days' \
                        f'=2&daily=temperature_2m_max,temperature_2m_min&timezone=GMT'

    r_weather = requests.get(url_weather_daily)
    weather_json = r_weather.json()

    response = {}

    temperature = {'max': weather_json['daily']['temperature_2m_max'][0],
                   'min': weather_json['daily']['temperature_2m_min'][0]}

    response['temperature'] = temperature
    response['new-api'] = client.is_enabled('nuevoapi', app_context)

    return response


if __name__ == '__main__':
    app.run(debug=False, port=5000)
