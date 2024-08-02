import logging
import signal 
import pyttsx3
import paho.mqtt.client as mqtt
import threading

from mqtt_text2speech import config

class Text2SpeechClient: 
    '''
    This class is responsible for connecting to the MQTT broker and listening for messages on the output topic.
    '''
    def __init__(self, *args, **kwargs): 

        # Initialize MQTT client
        self.client = mqtt.Client()
        self.client.username_pw_set(config.MQTT_BROKER_USERNAME, config.MQTT_BROKER_PASSWORD)
        # Set callback functions
        self.client.on_connect = self._on_broker_connect
        self.client.on_message = self._on_broker_message
        self.client.on_disconnect = self._on_broker_disconnect

        # Initialize local pyttsx3 engine
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", config.RATE)
        self.engine.setProperty("volume", config.VOLUME)
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[config.VOICE].id)
        # Set pyttsx3 callback functions
        self.engine.connect('finished-utterance', self._on_speech_end)
        self.engine.connect('error', self._on_speech_error) 

        # Connect Keyboard Interrupt signal to stop function
        signal.signal(signal.SIGINT, self.stop)

    def _on_broker_connect(self, client, userdata, flags, rc):
        logging.info(f"Connected with result code {rc}")
        self.client.subscribe(config.OUTPUT_TOPIC)

    def _on_broker_disconnect(self, client, userdata, rc):
        logging.info(f"Disconnected from broker with code {rc}")
        self.client.unsubscribe(config.OUTPUT_TOPIC)

    def _on_broker_message(self, client, userdata, msg):
        # Start a new thread to prevent blocking mqtt loop
        threading.Thread(target=self._speak, args=(msg.payload.decode(),)).start()

    def _on_speech_end(self, *args, **kwargs):
        logging.info("Finished speaking")
        # Send confirmation message
        self.client.publish(config.FINISHED_TOPIC, payload=None, qos=0, retain=False)

    def _on_speech_error(self, *args, **kwargs):
        logging.error("Error while speaking")

    def _speak(self, text):
        logging.info(f"Speaking: '{text}'")
        self.client.publish(config.STARTED_TOPIC, payload=None, qos=0, retain=False)
        self.engine.say(text)
        self.engine.runAndWait()

    def start(self): 
        logging.info("Starting MQTT Audioclient")
        self.client.connect(host=config.MQTT_BROKER_HOST, port=config.MQTT_BROKER_PORT, keepalive=60)
        self.client.loop_start()

    def stop(self, *args, **kwargs): 
        logging.info("Stopping MQTT Audioclient")
        self.client.disconnect()
        self.client.loop_stop()
        exit(0) # Quit the program
