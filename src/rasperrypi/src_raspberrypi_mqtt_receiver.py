import paho.mqtt.client as mqtt

# Pico Wが送信してくるトピック
TOPIC = "sensor/temperature"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    temperature = msg.payload.decode()
    print(f"Received from Pico W: {temperature} C")
    # TODO: ここで AWS IoT Core へ転送する処理を追加する

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# 自分自身(ラズパイ)のブローカーに接続
client.connect("localhost", 1883, 60)
client.loop_forever()