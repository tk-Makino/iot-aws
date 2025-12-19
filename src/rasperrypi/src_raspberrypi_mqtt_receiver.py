import paho.mqtt.client as mqtt
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

# --- 設定項目 ---
# Local MQTT (Pico W -> RPi)
LOCAL_TOPIC = "sensor/temperature"

# AWS IoT 設定
AWS_ENDPOINT = "YOUR_ENDPOINT.iot.ap-southeast-1.amazonaws.com" # AWSコンソールで確認
CLIENT_ID = "RaspberryPi_Gateway"
AWS_TOPIC = "pico/temperature"
CA_PATH = "certs/AmazonRootCA1.pem"
KEY_PATH = "certs/xxx-private.pem.key"
CERT_PATH = "certs/xxx-certificate.pem.crt"

# --- AWS IoT Client の初期化 ---
aws_client = AWSIoTMQTTClient(CLIENT_ID)
aws_client.configureEndpoint(AWS_ENDPOINT, 8883)
aws_client.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

# 接続設定
aws_client.configureAutoReconnectBackoffTime(1, 32, 20)
aws_client.configureOfflinePublishQueueing(-1)
aws_client.configureDrainingFrequency(2)
aws_client.configureConnectDisconnectTimeout(10)
aws_client.configureMQTTOperationTimeout(5)

print("Connecting to AWS IoT...")
aws_client.connect()
print("Connected to AWS IoT!")

# --- Local MQTT (Paho) のコールバック ---
def on_connect(client, userdata, flags, rc):
    print(f"Connected to local MQTT Broker (rc: {rc})")
    client.subscribe(LOCAL_TOPIC)

def on_message(client, userdata, msg):
    temperature = msg.payload.decode()
    print(f"Received from Pico W: {temperature} C")
    
    # AWS IoT へ転送
    payload = json.dumps({
        "device": "PicoW",
        "temperature": float(temperature)
    })
    aws_client.publish(AWS_TOPIC, payload, 1)
    print(f"Published to AWS IoT: {payload}")

# --- メイン処理 ---
local_client = mqtt.Client()
local_client.on_connect = on_connect
local_client.on_message = on_message

# ラズパイ内のブローカーに接続
local_client.connect("localhost", 1883, 60)
local_client.loop_forever()