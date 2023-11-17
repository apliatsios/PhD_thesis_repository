import json
from neo4j import GraphDatabase
import base64
import neo4j_config as config
import asyncio

logger = None
driver = None

data = {'platform': 'Thingspeak', 'channel': '1727524', 'timestamp': '2022-07-11T19:13:46Z', 'pm2.5': '480.00000', 'pm10': '902.00000',
        'so2': '981.00000', 'no2': '889.00000', 'o3': '51.00000', 'lat': 36.96, 'lng': 26.96}
data1 = {'platform': 'Thingspeak', 'channel': '1727524', 'timestamp': '2022-06-11T19:13:46Z', 'pm2.5': '0.00000', 'pm10': '0.00000',
        'so2': '0.00000', 'no2': '0.00000', 'o3': '0.00000', 'lat': 36.96, 'lng': 26.96}
data2_1 = {'platform': 'Ubidots', 'device': 'aegean-lopy4-node2', 'var': 'no2', 'value': '358.0', 'timestamp': '1655585208159'}
data2_2 ={'platform': 'Ubidots', 'device': 'aegean-lopy4-node2', 'var': 'o3', 'value': '724.0', 'timestamp': '1655585208159'}
data2_3 ={'platform': 'Ubidots', 'device': 'aegean-lopy4-node2', 'var': 'pm10', 'value': '1039.0', 'timestamp': '1655585208159'}
data2_4 ={'platform': 'Ubidots', 'device': 'aegean-lopy4-node2', 'var': 'pm2.5', 'value': '7.0', 'timestamp': '1655585208159'}
data2_5 ={'platform': 'Ubidots', 'device': 'aegean-lopy4-node2', 'var': 'so2', 'value': '607.0', 'timestamp': '1655585208159'}    
data2_6={'platform': 'Ubidots', 'device': 'aegean-lopy4-node2', 'var': 'position', 'value': {'lat': '36.95754', 'lng': '26.968904'}, 'timestamp': '2022-06-18 23:46:48'}
api_data = {'no2': 0.95, 'o3': 103, 'so2': 2.44, 'pm2_5': 18.55, 'pm10': 27.99, 'name': 'Agios_Savvas', 'api_name': 'open_weather', 'lat': 36.94479897403746, 'long': 26.98052565369983, 'timestamp': '2022-08-23T01:09:09'}

def decode(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('ascii')

def neo4j_init(logging):
    global driver
    global logger
    logger = logging
    driver = GraphDatabase.driver(decode(config.uri), auth=(decode(config.user), decode(config.password)), max_connection_pool_size=config.max_connection_pool_size)
    print("Connected on Neo4j Database")

def neo4j_destroy():
    global driver
    if driver is not None:
        driver.close()
        logger.info("NEO4J IS CLOSED")

def get_driver():
    global driver
    if driver is None:
        neo4j_init()
    return driver

def add_th_iot_data(tx, channel, platform, pm2_5, pm10, so2, no2, o3, lng, lat, timestamp):
    tx.run("MERGE (a:IoT_Entity{label: \"Iot_Entity\", name: \"Iot_Entity_\"+$channel})-[:hasPlatform]->(b:IoT_Platform{label: \"IoT_Platform\", name: $platform, channel: $channel})"
           "MERGE (a)-[:hasSensor]->(c:Sensor{label: \"Sensor\", name: \"PMS5003_\"+$channel})"
           "MERGE (c)-[:hasSensorProperty]->(d:SensorProperty{label: \"SensorProperty\", name: \"pm2.5\", value: $pm2_5, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (c)-[:hasSensorProperty]->(e:SensorProperty{label: \"SensorProperty\", name: \"pm10\", value: $pm10, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (a)-[:hasSensor]->(f:Sensor{label: \"Sensor\", name: \"MQ131_\"+$channel})"
           "MERGE (f)-[:hasSensorProperty]->(g:SensorProperty{label: \"SensorProperty\", name: \"o3\", value: $o3, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (a)-[:hasSensor]->(h:Sensor{label: \"Sensor\", name: \"MQ136_\"+$channel})"
           "MERGE (h)-[:hasSensorProperty]->(i:SensorProperty{label: \"SensorProperty\", name: \"no2\", value: $no2, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (h)-[:hasSensorProperty]->(j:SensorProperty{label: \"SensorProperty\", name: \"so2\", value: $so2, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (a)-[:hasLocation]->(k:Location{label: \"Location\", long: $lng, lat: $lat})",
           channel=channel, platform=platform, pm2_5=float(pm2_5), pm10=float(pm10), so2=float(so2), no2=float(no2), o3=float(o3), lng=float(lng), lat=float(lat), timestamp=timestamp)

def add_ubi_iot_data(tx, platform, device, var, value, timestamp):
    if var=='position':
        logger.info("UBIDOTS GEO COORDS")
        tx.run("MERGE (a:IoT_Entity{label: \"Iot_Entity\", name: \"Iot_Entity_\"+$device})-[:hasPlatform]->(b:IoT_Platform{label: \"IoT_Platform\", name: $platform, channel: $device})"
            "MERGE (a)-[:hasLocation]->(k:Location{label: \"Location\", long: $lng, lat: $lat})",
            platform=platform, device=device, var=var, value=value, timestamp=timestamp, lat = float(value['lat']),lng = float(value['lng']))
        logger.info("UBIDOTS GEO COORDS - DONE")
    else:
        logger.info("UBIDOTS SENSOR DATA")
        sensors = {"pm2.5":"PM5003", "pm10":"PM5003", "o3":"MQ131", "so2":"MQ136", "no2":"MQ136"}
        tx.run("MERGE (a:IoT_Entity{label: \"Iot_Entity\", name: \"Iot_Entity_\"+$device})-[:hasPlatform]->(b:IoT_Platform{label: \"IoT_Platform\", name: $platform, channel: $device})"
            "MERGE (a)-[:hasSensor]->(c:Sensor{label: \"Sensor\", name: $sensor+\"_\"+$device})"
            "MERGE (c)-[:hasSensorProperty]->(d:SensorProperty{label: \"SensorProperty\", name: $var, value: $value, unit: \"ug/m3\", timestamp: $timestamp})",
            platform=platform, device=device, var=var, value=float(value), timestamp=timestamp, sensor=sensors[var])
        logger.info("UBIDOTS SENSOR DATA - DONE")

def add_api_data(tx, name, api_name, pm2_5, pm10, so2, no2, o3, long, lat, timestamp):
    logger.info("API DATA")
    tx.run("MERGE (a:OpenData_Entity{label: \"OpenData_Entity\", name: \"OpenData_Entity_\"+$name})-[:hasPlatform]->(b:OpenData_Platform{label: \"OpenData_Platform\", name: $api_name})"
           "MERGE (a)-[:hasSensorProperty]->(d:SensorProperty{label: \"SensorProperty\", name: \"pm2.5\", value: $pm2_5, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (a)-[:hasSensorProperty]->(e:SensorProperty{label: \"SensorProperty\", name: \"pm10\", value: $pm10, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (a)-[:hasSensorProperty]->(g:SensorProperty{label: \"SensorProperty\", name: \"o3\", value: $o3, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (a)-[:hasSensorProperty]->(i:SensorProperty{label: \"SensorProperty\", name: \"no2\", value: $no2, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (a)-[:hasSensorProperty]->(j:SensorProperty{label: \"SensorProperty\", name: \"so2\", value: $so2, unit: \"ug/m3\", timestamp: $timestamp})"
           "MERGE (a)-[:hasLocation]->(k:Location{label: \"Location\", long: $long, lat: $lat})",
           name=name, api_name=api_name, pm2_5=float(pm2_5), pm10=float(pm10), so2=float(so2), no2=float(no2), o3=float(o3), long=float(long), lat=float(lat), timestamp=timestamp)
    logger.info("API DATA - DONE") 


def write_msg(msg):
    logger.info("creating session")
    try:
        if msg['platform'] == 'Thingspeak':
            with get_driver().session() as session:
                session.write_transaction(add_th_iot_data, msg['channel'], msg['platform'], msg['pm2.5'],
                    msg['pm10'], msg['so2'], msg['no2'], msg['o3'], msg['lng'], msg['lat'], msg['timestamp'])
        elif msg['platform'] == 'Ubidots':
            with get_driver().session() as session:
                session.write_transaction(add_ubi_iot_data, msg['platform'], msg['device'], msg['var'], msg['value'], msg['timestamp'])  
    except RuntimeError as err:
        logger.info(err)

def write_api_data(resp):
    logger.info("creating session")
    try:
        with get_driver().session() as session:
            session.write_transaction(add_api_data, resp['name'], resp['api_name'], resp['pm2.5'], resp['pm10'], resp['so2'], resp['no2'], resp['o3'], resp['long'], resp['lat'], resp['timestamp'])  
    except RuntimeError as err:
        logger.info(err)

 
# if __name__ == "__main__":
#     neo4j_init(logger)
#     write_api_data(api_data)

