import time
import paho.mqtt.client as mqtt
from kukavarproxy import KUKA  # Ensure this module is installed and working

# KUKA Robot Connection
robot_ip = '192.168.1.147'
robot = KUKA(robot_ip)

# Define monitored variables and their MQTT topics
monitored_vars = {
    "E_SPEED": {
        "topic": "extruder/motorSpeed",
        "transform": lambda x: x,  # No transformation needed
        "last_value": None
    },
    "E_ENABLE": {
        "topic": "extruder/motorEnable",
        "transform": lambda x: int(x == 'TRUE'),  # Convert to 1 or 0
        "last_value": None
    },
    "F_SPEED": {
        "topic": "extruder/fanSpeed",
        "transform": lambda x: x,  # No transformation needed
        "last_value": None
    }
}

# MQTT Configuration
mqttBroker = "192.168.1.20"
mqttPort = 1883

# Initialize MQTT Client (MQTT v3)
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to MQTT Broker!" if rc == 0 else f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid, rc, properties=None):
    print(f"Message published (MID: {mid}, RC: {rc})")

def monitor_and_publish_variables():
    """Monitor KUKA variables and publish changes to MQTT"""
    for var_name, config in monitored_vars.items():
        try:
            # Read current value from KUKA
            current_value = robot.read(var_name)
            
            # Transform the value if needed
            transformed_value = config["transform"](current_value)
            
            # Publish if value has changed
            if transformed_value != config["last_value"]:
                mqttc.publish(config["topic"], str(transformed_value), qos=1)
                print(f"Published {transformed_value} to {config['topic']}")
                config["last_value"] = transformed_value
                
        except Exception as e:
            print(f"Error reading {var_name}: {e}")

# Assign Callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# Connect to MQTT Broker
mqttc.connect(mqttBroker, mqttPort, 60)
mqttc.loop_start()

while True:
    try:
        monitor_and_publish_variables()
        time.sleep(1)
    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(2)  # Wait before retrying in case of error