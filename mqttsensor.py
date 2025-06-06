import paho.mqtt.client as mqtt
import time
import random
import multiprocessing as mp

# =============== Configuration (REPLACE WITH YOUR VALUES) ===============
SERVER_URL = "<username>.eu-latest.cumulocity.com"  # Cumulocity tenant URL
CLIENT_ID = "<>"              # Unique device identifier
DEVICE_NAME = "<>"            # Display name in Cumulocity
TENANT = "<your-tenant>"              # Tenant ID from Cumulocity
USERNAME = "<your-username>"          # Cumulocity username
PASSWORD = "<your-password>"          # Cumulocity password
# ========================================================================

# Global task queue for thread-safe operations (fixes Paho threading issues)
task_queue = mp.Queue()

def on_message(client, userdata, message):
    """Callback for incoming MQTT messages."""
    payload = message.payload.decode("utf-8")
    print(f" < Received message: {payload}")
    
    # Handle restart command (SmartREST template 510)
    if payload.startswith("510"):
        task_queue.put(perform_restart)

def perform_restart():
    """Simulate device restart using SmartREST templates 501/503."""
    print("Simulating device restart...")
    publish("s/us", "501,c8y_Restart", wait_for_ack=True)
    time.sleep(1)
    publish("s/us", "503,c8y_Restart", wait_for_ack=True)
    print("Restart completed")

def send_measurements():
    """Send simulated device measurements using SmartREST templates."""
    templates = [
        "211," + str(random.randint(10, 20)),  # Simple measurement
        "200,Temperature,c8y_Temperature," + str(random.randint(100,400)) + ",F",
        "200,Vibration,c8y_Vibration," + str(random.randint(0,2)) + ",ms2",
        "200,Voltage,c8y_Voltage," + str(random.randint(110,250)) + ",V",
        "200,Filament Consumption,c8y_Filament,50,%",
        "200,Current,c8y_Current," + str(random.randint(5,50)) + ",A",
        "200,Print Speed,c8y_PrintSpeed," + str(random.randint(0,1000)) + ",mmps",
        "200,Service Request 1,c8y_serReq1,25,",
        "200,Anomaly Score,c8y_Anomaly," + str(random.randint(40,60)) + ",%"
    ]
    for template in templates:
        publish("s/us", template)

def send_alarms():
    """Trigger sample alarms using SmartREST templates."""
    publish("s/us", "301,c8y_PowerDisconnect,Printer1 Disconnected")
    publish("s/us", "302,c8y_NeedRepair,Printer1 Needs Repair")

def send_events():
    """Create sample events using SmartREST templates."""
    events = [
        "400,c8y_Status,Printer Turned Off",
        "400,c8y_Status,Printer Turned On",
        "400,c8y_Status,Printer Unplugged",
        "400,c8y_P1SerReq,Service Request from Printer"
    ]
    for event in events:
        publish("s/us", event)

def publish(topic, message, wait_for_ack=False):
    """Publish MQTT message with optional QoS 2 acknowledgement."""
    qos = 2 if wait_for_ack else 0
    message_info = client.publish(topic, message, qos=qos)
    
    if wait_for_ack:
        print(f" > Awaiting ACK for {message_info.mid}")
        message_info.wait_for_publish()
        print(f" < Received ACK for {message_info.mid}")

def on_publish(client, userdata, mid):
    """Callback when messages are published."""
    print(f" > Published message: {mid}")

# Initialize MQTT client
client = mqtt.Client(CLIENT_ID)
client.username_pw_set(f"{TENANT}/{USERNAME}", PASSWORD)
client.on_message = on_message
client.on_publish = on_publish

# Connect and register device
try:
    client.connect(SERVER_URL)
    client.loop_start()
    
    # Device registration sequence
    publish("s/us", f"100,{DEVICE_NAME},c8y_MQTTDevice1", wait_for_ack=True)
    publish("s/us", "110,3DP 123,3DP,Rev0.1")
    publish("s/us", "115,3DP_Fw_1,v2.0,www.3dp.com")
    publish("s/us", "116,3DP_Sw_1,v2.0,www.3dp.com")
    publish("s/us", "113,agent.requiredinterval=10")
    publish("s/us", "112,42.36,-71.05,0")
    publish("s/us", "114,c8y_Restart")
    print("Device registered successfully!")
    
    # Subscribe to device control channel
    client.subscribe("s/ds")
    
    # Main loop
    while True:
        send_measurements()
        send_events()
        send_alarms()
        time.sleep(5)

except KeyboardInterrupt:
    print("\nDisconnecting...")
    client.disconnect()
    client.loop_stop()
