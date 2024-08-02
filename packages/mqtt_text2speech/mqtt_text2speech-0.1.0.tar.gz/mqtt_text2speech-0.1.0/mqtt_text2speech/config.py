import os
from dotenv import load_dotenv

load_dotenv() 

def load_env_var(env_var, default_val=None): 
    val = os.environ.get(env_var, default_val) 
    if val is None:
        raise ValueError(f"Environment variable {env_var} is not set.")
    return val

# MQTT Broker configuration
MQTT_BROKER_HOST = str(load_env_var("MQTT_BROKER_HOST", "localhost"))
MQTT_BROKER_PORT = int(load_env_var("MQTT_BROKER_PORT", 1883))
MQTT_BROKER_USERNAME = str(load_env_var("MQTT_BROKER_USERNAME"))
MQTT_BROKER_PASSWORD = str(load_env_var("MQTT_BROKER_PASSWORD"))

# MQTT Topics for audio output
OUTPUT_TOPIC = str(load_env_var("OUTPUT_TOPIC"))
STARTED_TOPIC = str(load_env_var("STARTED_TOPIC"))
FINISHED_TOPIC = str(load_env_var("FINISHED_TOPIC"))

# pyttsx3 configuration
RATE = int(load_env_var("RATE", 150))
VOLUME = float(load_env_var("VOLUME", 1.0))
VOICE = int(load_env_var("VOICE", 0))


           