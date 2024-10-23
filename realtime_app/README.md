# Realtime app
## How to run
- Step 1 build docker image: ```docker build -t kafka-consumer-app .```
- Step 2 run docker container: ```docker run -d --name kafka-consumer-app kafka-consumer-app```

### Note:
-  before run please change the bootstrap_servers
- auto produce to topic with ```python auto_produce.py``` data extract from `first.json`