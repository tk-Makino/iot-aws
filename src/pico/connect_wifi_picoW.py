import machine
import time
import network
from umqtt.simple import MQTTClient

# --- 設定項目 ---
SSID = "あなたのWiFi名"
PASSWORD = "あなたのパスワード"
MQTT_BROKER = "192.168.x.x"  # ラズパイのIPアドレス
CLIENT_ID = "PicoW_Sensor"
TOPIC = b"sensor/temperature"

# --- ADT7410 I2C設定 ---
# I2C0 (SDA: GP0, SCL: GP1) を想定
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
ADT7410_ADDR = 0x48

def get_temperature():
    # ADT7410から2バイト読み取り
    data = i2c.readfrom_mem(ADT7410_ADDR, 0x00, 2)
    # 13bit/16bitモードに合わせて計算 (13bitの場合)
    temp_raw = (data[0] << 8 | data[1]) >> 3
    if temp_raw & 0x1000: # 負の値の処理
        temp_raw -= 8192
    return temp_raw * 0.0625

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(1)
    print("WiFi Connected. IP:", wlan.ifconfig()[0])

# --- メイン処理 ---
connect_wifi()

client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.connect()

print("Starting sensor loop...")
try:
    while True:
        temp = get_temperature()
        print(f"Temperature: {temp:.2f} C")
        
        # MQTTで送信
        client.publish(TOPIC, str(temp).encode())
        
        time.sleep(5) # 5秒おきに送信
except Exception as e:
    print("Error:", e)
finally:
    client.disconnect()