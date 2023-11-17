import os.path
import enum
# Using enum class create enumerations
class Platforms(enum.Enum):
   Ubidots = "Ubidots"
   Thingspeak = "Thingspeak"

class Platforms_Variables(enum.Enum):
    Ubidots=["no2", "o3", "pm10", "pm2_5", "so2", "position"]
    Thingspeak = {'field1': 'pm2.5', 'field2': 'pm10', 'field3': 'so2', 'field4': 'no2', 'field5': 'o3',
              'field6': 'lat', "field7": 'lng', 'status': 'AQI', 'created_at': 'timestamp'}

mqtt_keepalive = 60
# Ubidots: Maximum devices per account = 3
# Thingspeak: Maximum devices per account = 4
clients=[
{"broker_type":Platforms.Ubidots.value,"broker":"industrial.api.ubidots.com","port":8883,"username":"BBFF-gsZga86SXWAHpLQYff8SmnMNcR7Q4C",
"pass":"","clientId":"Ubidots_1","devices":["aegean-lopy4-node1","arduino_wifi_mqtt","arduino_eth_http"]},

{"broker_type":Platforms.Ubidots.value,"broker":"industrial.api.ubidots.com","port":8883,"username":"BBFF-PAjkojxVEYkeSlGX6geyAwYDe5oZM0",
"pass":"","clientId":"Ubidots_2","devices":["aegean-lopy4-node2"]},

# DL Account
{"broker_type":Platforms.Thingspeak.value,"broker":"mqtt3.thingspeak.com","port":8883,"username":"DAgaNgE1BTUaPScaHB8zCB4",
"pass":"gHzZYq6FGSrg3R6C3sdpj8if","clientId":"DAgaNgE1BTUaPScaHB8zCB4","channels":["1270095","1698145","1726471","1727202"]},

# icsd Account
{"broker_type":Platforms.Thingspeak.value,"broker":"mqtt3.thingspeak.com","port":8883,"username":"HSQvGgIlJzMQLxozEAQmDSg",
"pass":"ehsENVZ/0ucYx9fjPusLwH8U","clientId":"HSQvGgIlJzMQLxozEAQmDSg","channels":["1727524"]},
]

