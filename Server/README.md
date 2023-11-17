# Creating a Linux service with systemd
All services are located in <u>/etc/systemd/system</u>. 
## Creating a service
In order to create a service, we must create a .service file in that directory, using the following command:
```
sudo nano /etc/systemd/system/mydaemon.service
```

## Reload the service files to include the new service.
```
sudo systemctl daemon-reload
```

## Start your service
```
sudo systemctl start your-service.service
```

## To check the status of your service
```
sudo systemctl status example.service
```

## To enable your service on every reboot
```
sudo systemctl enable example.service
```

## To disable your service on every reboot
```
sudo systemctl disable example.service
```