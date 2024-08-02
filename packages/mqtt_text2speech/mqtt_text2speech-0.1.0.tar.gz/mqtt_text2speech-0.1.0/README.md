## Simple MQTT Text2Speech Client 

Dieser MQTT Client subscribed ein 'OutputTopic', wo Textnachrichten published werden können, die der Client dann anschließend mit pyttsx3 ausgibt. 
Der Beginn der Sprachausgabe durch den MQTT Client wird unter dem 'StartedTopic' signalisiert. 
Sobald die Sprachausgabe beendet wurde, signalisiert der MQTT Client dies unter dem 'FinishedTopic'.  

## Environment Variables

The parameters of the MQTT Text2Speech client are read as environment variables from a `.env` file. 
The following environment variables need to be defined inside the `.env` file:

```
OUTPUT_TOPIC = "/output-topic-msgs-are-published-to"
STARTED_TOPIC = "/started-topic"
FINISHED_TOPIC = "/finished-topic"

MQTT_BROKER_HOST = "host-ip-address"
MQTT_BROKER_PORT = "1883"
MQTT_BROKER_USERNAME = "mqtt-broker-username"
MQTT_BROKER_PASSWORD = "mqtt-broker-password"

RATE = 150 
VOLUME = 1.0 
VOICE = 0
```

## Starting the MQTT Text2SpeechClient

```python
import logging
from mqtt_text2speech.client import Text2SpeechClient

# Logging configuration to see output (optional)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

# Start MQTT Text2SpeechClient with environment variables configured in .env file
client = Text2SpeechClient()
client.start()

# Do stuff (Loop to keep main thread busy)
while True: 
    pass

# Connection to MQTT Broker will be closed if main thread ends
client.stop()
```

