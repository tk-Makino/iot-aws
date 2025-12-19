from machine import I2C, Pin
import time
import network
from umqtt.simple import MQTTClient

# --- 設定項目 ---
SSID = "ZXXX"
PASSWORD = "1XXXXX"
MQTT_BROKER = "192.168.XXXXX"  # ラズパイのIPアドレス
CLIENT_ID = "PicoW_Sensor"
TOPIC = b"sensor/temperature"

# --- ADT7410 I2C設定 ---
I2C_SDA = 16
I2C_SCL = 17
I2C_CH = 0
I2C_ADDR = 0x48  # ADT7410のI2Cアドレス

i2c = I2C(I2C_CH, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)
i2c.scan()

sensor = i2c.writeto_mem(I2C_ADDR, 0x03, bytearray([0x80]))  # 16bitモード設定

def get_temperature():
    raw = i2c.readfrom_mem(I2C_ADDR, 0x00, 2)
    msb = raw[0]
    lsb = raw[1]
    temparature = (msb << 8) | lsb

    if (temparature >=32768):
        temparature -= 65536

    temparature = temparature/128.0  # 16bitモードの場合
    return temparature

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