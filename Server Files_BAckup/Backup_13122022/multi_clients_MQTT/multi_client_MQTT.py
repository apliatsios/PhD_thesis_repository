#from asyncio.windows_events import NULL
import paho.mqtt.client as mqtt
import multi_client_config as config
import parse_data as prd
import logging
import concurrent.futures
import sys
sys.path.insert(0, r'/home/apliatsios/dlyberis/Neo4j')
import Neo4j_transactions as neo4j

# List to get printed messages in some form of order
global final_data

final_data = []
msg_counter = 0
msg_parsed_counter = 0

def on_connect(client, userdata, flags, rc):
    logging.info("Result from connect: {}".format(mqtt.connack_string(rc)))
    if rc == 0:
        logging.info("[INFO] Connected to broker")
        for i in range(len(config.clients)):
            if config.clients[i]["client"] == client:
                if config.clients[i]["broker_type"] == config.Platforms.Ubidots.value:
                    # Get devices' names in order to construct subscription topics
                    devices = config.clients[i]["devices"]
                    # Iterate devices' names and subscribe to the corresponding topic
                    for dev in devices:
                        client.subscribe(
                            "/v1.6/devices/{}/+".format(dev), qos=0)
                        logging.info(
                            "Subscribed to topic:\"/v1.6/devices/{}/+\"".format(dev))
                    break
                elif config.clients[i]["broker_type"] == config.Platforms.Thingspeak.value:
                    # Get channels' id in order to construct subscription topics
                    channels = config.clients[i]["channels"]
                    # Iterate channels and subscribe to the corresponding topic
                    for ch in channels:
                        client.subscribe(
                            "channels/{}/subscribe".format(ch), qos=0)
                        logging.info(
                            "Subscribed to topic:\"channels/{}/subscribe\"".format(ch))
                    break
    else:
        logging.error("[ERROR] Error, connection failed")


def on_subscribe(client, userdata, mid, granted_qos):
    logging.info("I've subscribed with QoS: {}".format(granted_qos[0]))


def on_message(client, userdata, msg):
    logging.info("Message received. Topic: {}. Payload: {}".format(msg.topic, str(msg.payload.decode("utf-8"))))
    global msg_counter
    msg_counter = msg_counter + 1
    parsed_data = prd.get_data(msg.topic, str(msg.payload.decode("utf-8")))
    if parsed_data is not None:
        # REPLACE THIS WITH NEO4J function
        # final_data.append(parsed_data)
        # print(final_data)
        logging.info("Parsed_Message: {}".format(parsed_data))
        if 'AQI' not in parsed_data:
            logging.info("Ready to write Parsed_Message")
            neo4j.write_msg(parsed_data)
            logging.info("Parsed_Message was written")
        global msg_parsed_counter
        msg_parsed_counter = msg_parsed_counter + 1
    logging.info("Total_msgs:{0}, Total_parsed_msgs:{1}".format(
        msg_counter, msg_parsed_counter))


def Create_connections():
    logging.info("Start Create_connections")
    for i in range(len(config.clients)):
        # Extract Data from each client to prepare connections
        mqtt_server_host = config.clients[i]["broker"]
        mqtt_server_port = config.clients[i]["port"]
        userName = config.clients[i]["username"]
        passWord = config.clients[i]["pass"]
        clientId = config.clients[i]["clientId"]
        client = mqtt.Client(clientId, mqtt.MQTTv311)
        config.clients[i]["client"] = client
        try:
            client.connect_async(host=mqtt_server_host, port=mqtt_server_port, keepalive=config.mqtt_keepalive)
            logging.info("{} is connected on {}:{}.".format(config.clients[i]["clientId"], config.clients[i]["broker"], config.clients[i]["port"]))
        except:
            logging.error("Connection Fialed to broker ", mqtt_server_host)
            continue
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.username_pw_set(userName, passWord)
        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    logging.info("End Create_connections")

def client_loop(config_client):
        config_client["client"].loop_forever()


if __name__ == "__main__":
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s - %(thread)d]  [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    fileHandler = logging.FileHandler('/home/apliatsios/dlyberis/app.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(logging.INFO)
    neo4j.neo4j_init(logging)
    Create_connections()
    with concurrent.futures.ThreadPoolExecutor(5,thread_name_prefix='ThreadPool') as executor:
        executor.map(client_loop,config.clients)
    while True:
        try:
            # pass
            print(final_data)
        except:
            print("Application Stopped")
            print(final_data)
            neo4j.neo4j_destroy()
        finally:
            neo4j.neo4j_destroy()
            
            
