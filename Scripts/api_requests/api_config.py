import os.path
import enum

Loc = {'Agios_Savvas': {'lat': 36.94479897403746, 'lon': 26.98052565369983,'api_name':'open_weather'},
       'Airport': {'lat': 36.96411328843375, 'lon': 26.940153270090374,'api_name':'ninjas_airq'},
       'Myrties': {'lat': 36.990931578588416, 'lon': 26.93151331395161,'api_name':'open_weather'},
       'Melitsaxas': {'lat': 36.986894208621614, 'lon': 26.928929475287934,'api_name':'ninjas_airq'},
       'Pothia_01': {'lat': 36.94906497634183, 'lon': 26.982050079436924,'api_name':'open_weather'},
       'Pothia_02': {'lat': 36.95297945129611, 'lon': 26.975620533540777,'api_name':'ninjas_airq'},
       'Pothia_03': {'lat':36.960876, 'lon':26.971832,'api_name':'open_weather'},
       'Agios_Athanasios': {'lat':36.95664154400455, 'lon':26.965767803949493,'api_name':'ninjas_airq'},
       'Chora_01': {'lat':36.9636846089928, 'lon':26.960327032094618,'api_name':'open_weather'},
       'Taxiarchis': {'lat':36.96502031893271, 'lon':26.95289955137949,'api_name':'ninjas_airq'},
       'Port_Authority': {'lat':36.94657487279934, 'lon':26.984530254135713,'api_name':'open_weather'}
       }
# Using enum class create enumerations

class SupportedApis(enum.Enum):

    def __init__(self, api_name, url, key, headers):
        self.api_name = api_name
        self.url = url
        self.key = key
        self.headers = headers

    WEATHERBIT = ('weatherbit', 'https://air-quality.p.rapidapi.com/current/airquality', 'f2f1f98281msh84645eabe6802dep1124ddjsne5508c2423ec', {'X-RapidAPI-Host': 'air-quality.p.rapidapi.com','X-RapidAPI-Key': 'f2f1f98281msh84645eabe6802dep1124ddjsne5508c2423ec'})
    IQAIR = ('iqair', 'http://api.airvisual.com/v2/nearest_city', 'f55e45be-30ef-416d-b31e-7767c447bb91', {})
    NINJAS_AIRQ = ('ninjas_airq','https://api.api-ninjas.com/v1/airquality','SVVP4kvv853PkuYseZEsSg==EdAlT1L6x6BqeDwN', {'X-Api-Key':'SVVP4kvv853PkuYseZEsSg==EdAlT1L6x6BqeDwN'})
    OPEN_WEATHER = ('open_weather', 'http://api.openweathermap.org/data/2.5/air_pollution', '740af68f7f2cda5d6641fc0c52c85914', {})  
