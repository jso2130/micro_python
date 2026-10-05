from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

counter = 0
time_cnt = 0
red_on = 0

def timer_10ms():
    return

def timer_100ms():
    flash.value(not flash.value())

def timer_500ms():
    red.value(not red.value())


while True:
    time.sleep_ms(1)      # 1ms 동안 대기
    time_cnt += 1

    if time_cnt % 100 == 0:
        timer_100ms()

    if time_cnt % 500 == 0:
        timer_500ms()
