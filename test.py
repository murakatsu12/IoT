import time
import board
import busio
import adafruit_adt7410

# I2Cバスの初期化
i2c = busio.I2C(board.SCL, board.SDA)

# センサーの初期化（アドレス 0x48）
adt = adafruit_adt7410.ADT7410(i2c, address=0x48)

# 精度を16ビット（高精度）に設定
adt.high_resolution = True

print("--- ADT7410 温度測定開始 ---")

try:
    while True:
        temp = adafruit_adt7410.ADT7410(i2c, address=0x48).temperature
        print(f"現在の温度: {temp:.2f} ℃")
        time.sleep(2)
except KeyboardInterrupt:
    print("終了します")