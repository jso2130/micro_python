from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

while True:
    flash.value(1)          # 켜기
    time.sleep_ms(100)      # 100ms 동안 대기
    flash.value(0)          # 끄기
    time.sleep_ms(100)      # 100ms 동안 대기
