# eth communication for sending image

## 1. Wifi Setting
Editing /etc/rc.local
```
#sudo vi /etc/rc.local
sudo iw reg set US
exit 0
```
and reboot the system  

## 2. Package Installing

```
#sudo apt-get update
#sudo apt-get install -y numpy python3-opencv python-opencv
```

## 3. Executing server.py
```
#ifconfig
(check wlan0 ipaddress)
#./server.py
```


## 4. Execting client.py
Client must have camera module.  
```
#./client.py -i [server wlan0 ip address]
```
