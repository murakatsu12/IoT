import RPi.GPIO as GPIO
import time

# GPIO番号の定義
PUMP_PIN = 4

# 初期設定
GPIO.setwarnings(False) # 既に使用されている場合の警告を無視
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_PIN, GPIO.OUT)

print("--- リレー動作テスト開始 ---")
print("1秒おきに ON/OFF を繰り返します。")
print("中止するには Ctrl + C を押してください。")

try:
    while True:
        # 動きが逆なので、ONのときにLOWにする
        print("ON (カチッ)")
        GPIO.output(PUMP_PIN, GPIO.LOW)  # HIGHからLOWに変更
        time.sleep(10)
        
        print("OFF (カチッ)")
        GPIO.output(PUMP_PIN, GPIO.HIGH) # LOWからHIGHに変更
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\nユーザーにより中断されました。")
finally:
    GPIO.cleanup() # ピンの設定をリセット
    print("GPIOをクリーニングして終了します。")