# Neo4j Docker on VPS

## Install Docker Engine

1. Set up the repository

  ```sh
  sudo apt-get update
  sudo apt-get install ca-certificates curl gnupg lsb-release
  ```
  
2. Add Docker’s official GPG key:

  ```sh
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  ```

3. Use the following command to set up the stable repository.

  ```sh
  echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  ```

4.

  ```sh
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
  ```

5. List the versions available in your repo:

  ```sh
  apt-cache madison docker-ce
  ```  

6. Install a specific version using the version string:

  ```sh
  sudo apt-get install docker-ce=<VERSION_STRING> docker-ce-cli=<VERSION_STRING> containerd.io docker-compose-plugin
  ```  

7. Verify that Docker Engine is installed correctly by running the hello-world image:

  ```sh
  sudo docker run hello-world
  ```  

## Upgrade Docker Engine

  ```sh
  sudo apt-get update
  ```

## Create Neo4j container

  ```sh
  docker run \
      --name aristeia \
      --restart always \
      -p7474:7474 -p7687:7687 \
      -d \
      -v $HOME/neo4j/data:/data \
      -v $HOME/neo4j/logs:/logs \
      -v $HOME/neo4j/import:/var/lib/neo4j/import \
      -v $HOME/neo4j/plugins:/plugins \
      --env NEO4JLABS_PLUGINS='["apoc","n10s","graph-data-science"]' \
      --env-file /home/apliatsios/dlyberis/my_env.env \
      neo4j:latest
  ```

## Copy ontology in Docker

  ```sh
  sudo docker cp SSNT_ontology_version1_DL.owl CONTAINER ID:/usr/share
  ```

## Remove Neo4j Docker
  
  Stop Docker container

  ```sh
  sudo docker stop aristeia
  ```

  Remove Container from the host node  

  ```sh
  sudo docker rm aristeia
  ```

  Remove image from the host node

  ```sh
  sudo docker rmi neo4j
  ```

  Delete folder

  ```sh  
  sudo rm -r neo4j 
  ```

# Run python code as Service on Ubuntu

Create a service file for the systemd as following. The file must have .service extension under /lib/systemd/system/ directory

  ```sh  
  sudo nano /lib/systemd/system/MQTTListener.service 
  ```

Add the following content in it

  ```sh  
  [Unit]
  Description = This service subscribes to topics on IoT Platforms and collects data.
  After = network.target

  [Service]
  Type = simple
  ExecStart = python3 /home/apliatsios/dlyberis/multi_clients_MQTT/multi_client_MQTT.py
  User = apliatsios
  Group = apliatsios
  Restart = on-failure
  SyslogIdentifier =MQTT_Listener.log
  RestartSec = 5
  TimeoutStartSec = infinity

  [Install]
  WantedBy = multi-user.target 
  ```

Report system service logs by extracting them from the systemd journaling system

  ```sh
  journalctl -u MQTTListener.service -f
  ```

Create a service file for the systemd as following. The file must have .service extension under /lib/systemd/system/ directory

  ```sh  
  sudo nano /lib/systemd/system/ApiRequest.service 
  ```

Add the following content in it

  ```sh  
  [Unit]
  Description = This service collects Open source air quality data
  After = network.target

  [Service]
  Type = simple
  ExecStart = python3 /home/apliatsios/dlyberis/api_requests/api_scheduler.py
  User = apliatsios
  Group = apliatsios
  Restart = on-failure
  SyslogIdentifier = api_request.log
  RestartSec = 5
  TimeoutStartSec = infinity

  [Install]
  WantedBy = multi-user.target 
  ```

  Report system service logs by extracting them from the systemd journaling system

  ```sh
  journalctl -u ApiRequest.service -f
  ```

Reload the systemctl daemon to read new file. You need to reload this deamon each time after making any changes in in .service file.

  ```sh
  sudo systemctl daemon-reload
  ```

Enable the service to start on system boot, also start the service using the following commands
Finally check the status of your service.

  ```sh 
  sudo systemctl enable MQTTListener.service
  sudo systemctl start MQTTListener.service
  sudo systemctl status MQTTListener.service
  ```


Reload the systemctl daemon to read new file. You need to reload this deamon each time after making any changes in in .service file.

  ```sh
  sudo systemctl daemon-reload
  ```

Enable the service to start on system boot, also start the service using the following commands  
Finally check the status of your service.

  ```sh
  sudo systemctl enable ApiRequest.service
  sudo systemctl start ApiRequest.service
  sudo systemctl status ApiRequest.service
  ```


Use below commands to stop and restart your service manual.

  ```sh
  sudo systemctl stop ApiRequest.service
  sudo systemctl restart ApiRequest.service
  ```