# IOT-Platform
A server-less IoT solution development and management platform offers core functionality for managing the entire lifecycle of IoT solution development. This project is an attempt to to build a Distributed IoT platform that enables users to write programs and algorithms that use it in various domains of automation. 

The platform consists of a Django based web framework UI; and various modules like- Scheduler, Load Balancer, Monitoring service, Logging service, Deployer, Action and Notification Manager, Databases, Runtime Servers.

## Technologies 
1) Python3 and its Libraries
2) Django for Web Framework and Frontend
3) Kafka for Backend Communication
4) SqLite3 to store Structured Data

## Launch
How to run the project?

**Dependencies**

Before plugging into the project make sure you have the following requirements updated: (run the command aside if not)

apt-get -y update : execute if running any of the below.
1) Python3: apt-get -y install python3 
2) Python pip: pip3 install confluent-kafka
3) psutil: pip3 install psutil
4) schedule: pip3 install schedule
5) datetime: pip3 install DateTime
6) twilio: pip3 install twilio
7) glob3: pip3 install glob3
8) sqlite3: apt-get -y install sqlite3
9) Confluent-Kafka: pip3 install confluent-kafka

**Clone**

Clone this repo to your local machine using
```code
git clone https://github.com/SmritiAgrawal04/IOT-Platform.git
```

**Activate/Plug**

In your installed Kafka Directory, open a new terminal and start the zookeeper and server using the following commands- 
```code
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

Now in the cloned repo /IOT_Platform/ directory open a new terminal and run the command-
```code
sh start.sh
```
Wait until a link pops up on the terminal, Ctrl+click on it to start..

**Deactivate/Unplug**

In the same terminal where you executed 'start' script, press Ctrl+C and run the command- 
```code
sh stop.sh
```

##Architecture
<p align="center">
  <img src="/home/smriti/Downloads/Architecture.png" width="350" title="Architecture Diagram">
</p>


