from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0

def timer_100ms():
    flash.value(not flash.value())

def timer_500ms():
    red.value(not red.value())
    time.sleep_ms(300)  # 이 함수가 300ms 걸리는 일을 한다고 가정


while True:
    time.sleep_ms(1)
    time_cnt += 1

    if time_cnt % 100 == 0:
        timer_100ms()

    if time_cnt % 500 == 0:
        timer_500ms()
