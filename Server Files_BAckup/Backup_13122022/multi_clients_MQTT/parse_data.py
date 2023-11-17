import re
import json
from time import time
import multi_client_config as config
import time_conversions as tm

def get_data(topic, msg):
    # Identify platform from topic
    if "/v1.6/devices/" in topic:
        # Extract data from topic and payload
        return ubidots_data(topic, msg)
    elif "channels/" in topic:
        return thingspeak_data(topic, msg)


def ubidots_data(topic, msg):
    data = {}
    gps_data={}
    # Remove punctuation from topic
    topic1 = topic.replace(".", "")
    topic_list = topic1.split("/")
    var = topic_list[-1]

    if var not in config.Platforms_Variables.Ubidots.value:
        return None

    data["platform"] = config.Platforms.Ubidots.value
    # Get device's and variable's names
    data["device"] = topic_list[-2]
    if var=='pm2_5':
        data["var"] = 'pm2.5'
    else:
        data["var"] = var
    if var == "position":
        # Get lng nad lat coordinates
        gps_coords = re.findall("(\W\w{3}\W\S\s\d[0-9]*\S[0-9]*)", str(msg))
        # For each match
        for i in gps_coords:
            # Remove spaces, quotes and colon character
            coord = i.replace(" ", "").replace("\"", "").rsplit(":")
            gps_data[coord[0]] = coord[1]
        data["value"] = gps_data
    else:
        value = re.findall("\"value\": (\d[0-9]*\S\d[0-9]*)", msg)
        data["value"] = value[0]
    timestamp = re.findall("\"timestamp\": (\d[0-9]*)", msg)
    data["timestamp"] = str(tm.tm2daytime(int(timestamp[0])))
    return data


def thingspeak_data(topic, msg):
    """
    Remove from json data all the records with None value
    :data: (Dictionary) Initial json data
    :return: It returns a new dictionary with the remained data
    """
    # create a stucture for cleaned data
    data = {}
    data["platform"] = config.Platforms.Thingspeak.value
    topic_list = topic.split("/")
    data["channel"] = topic_list[1]
    payload = json.loads(msg.replace("Payload: ", ""))
    # iterate all elements of 'data' dictionary
    for key, value in payload.items():
        if key in config.Platforms_Variables.Thingspeak.value:             
            if value is not None:
                if key=="created_at":
                    data.update({config.Platforms_Variables.Thingspeak.value[key]: tm.utc2local(value)}) 
                else:
                    data.update({config.Platforms_Variables.Thingspeak.value[key]: value})
    return data
