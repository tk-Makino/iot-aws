import network
import time
import machine

# --- 設定項目 ---
SSID = "あなたのWi-Fi名"
PASSWORD = "あなたのパスワード"
# ----------------

def connect_wifi():
    # pico WでWi-Fiに接続する関数
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f'Connecting to {SSID}...')
        wlan.connect(SSID, PASSWORD)
        
        # 接続待ち（最大10秒）
        attempt = 0
        while not wlan.isconnected() and attempt < 10:
            print("Waiting for connection...")
            time.sleep(1)
            attempt += 1

    if wlan.isconnected():
        print('Connected!')
        print('IP Address:', wlan.ifconfig()[0])
        # 接続に成功したら内蔵LEDを点灯させる（Pico W専用）
        led = machine.Pin("LED", machine.Pin.OUT)
        led.on()
    else:
        print('Failed to connect.')

# 実行
connect_wifi()