from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

counter = 0
red_on = 0

# 구간 시작
while True:
    flash.value(1)          # 4번 핀에 HIGH(1) Signal을 보내 LED를 켭니다.

    if(red_on == 1):
        red.value(0)

    time.sleep_ms(100)      # 100ms 동안 대기

    flash.value(0)          # 4번 핀에 LOW(0) Signal을 보내 LED를 끕니다.

    if(red_on == 1):
        red.value(1)
        red_on = 0

    time.sleep_ms(100)      # 100ms 동안 대기

    counter += 1

    if counter > 2:
        counter = 0
        red_on = 1
