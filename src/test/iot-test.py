from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time
import json

# 設定値（自分の環境に合わせて書き換えてください）
ENDPOINT = "xxxxxxxxxxxxxx-ats.iot.ap-northeast-1.amazonaws.com" # IoT Coreの設定画面にあるエンドポイント
CLIENT_ID = "MyRaspberryPi"
PATH_TO_CERT = "./certs/xxx-certificate.pem.crt"
PATH_TO_KEY = "./certs/xxx-private.pem.key"
PATH_TO_ROOT = "./certs/AmazonRootCA1.pem"
TOPIC = "test/topic"

# 接続の確立
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=PATH_TO_CERT,
    pri_key_filepath=PATH_TO_KEY,
    client_bootstrap=client_bootstrap,
    ca_filepath=PATH_TO_ROOT,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=6
)

print(f"Connecting to {ENDPOINT} with client ID '{CLIENT_ID}'...")
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")

# データの送信
message = {"message": "Hello from Raspberry Pi!", "value": 123}
print(f"Publishing message to topic '{TOPIC}': {message}")
mqtt_connection.publish(
    topic=TOPIC,
    payload=json.dumps(message),
    qos=mqtt.QoS.AT_LEAST_ONCE
)

time.sleep(2)

# 切断
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("Disconnected!")
