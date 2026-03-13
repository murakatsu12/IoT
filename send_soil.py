import time
import board
import busio
import digitalio
import adafruit_adt7410
import adafruit_mcp3xxx.mcp3208 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import requests

# --- 初期化 ---
i2c = busio.I2C(board.SCL, board.SDA)
adt = adafruit_adt7410.ADT7410(i2c, address=0x48)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP.MCP3208(spi, cs)
soil_sensor = AnalogIn(mcp, MCP.P0)

pump = digitalio.DigitalInOut(board.D26)
pump.direction = digitalio.Direction.OUTPUT
PUMP_ON, PUMP_OFF = False, True # 逆論理
pump.value = PUMP_OFF

# --- 設定 ---
GAS_URL = "https://script.google.com/macros/s/AKfycbw-VpBc_zdOtEmRQok8LarwGwlzibfwsuRDG0oZv5Gw_-pO7QV-I6m47uAQ_3ZclqFI/exec"
SOIL_THRESHOLD_PC = 20
WATERING_TIME = 3

def get_soil_percent(raw_value):
    # 土の中での「湿っている」に合わせて数値を調整
    WET_MAX = 35000  # ここを大きくすると、今の土の%が上がります
    DRY_MIN = 56300  
    percent = (DRY_MIN - raw_value) / (DRY_MIN - WET_MAX) * 100
    return int(max(0, min(100, percent)))

def main():
    print("システム稼働中...")
    try:
        while True:
            temp = adt.temperature
            soil_pc = get_soil_percent(soil_sensor.value)
            print(f"温度: {temp:.1f}℃ | 土壌: {soil_pc}%")

            if soil_pc < SOIL_THRESHOLD_PC:
                print("!! 水やり開始 !!")
                pump.value = PUMP_ON
                time.sleep(WATERING_TIME)
                pump.value = PUMP_OFF

            # GAS送信 (名前をGAS側の変数と一致させる)
            payload = {"temperature": round(temp, 1), "soil_moisture": soil_pc}
            try:
                requests.post(GAS_URL, json=payload, timeout=10)
            except Exception as e:
                print(f"送信失敗: {e}")

            time.sleep(600)
    except KeyboardInterrupt:
        pass
    finally:
        pump.value = PUMP_OFF

if __name__ == "__main__":
    main()