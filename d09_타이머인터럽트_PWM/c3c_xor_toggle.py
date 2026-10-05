from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0

def timer_100ms():
    flash.value(flash.value() ^ 1)  # XOR 1 : 0 ↔ 1 뒤집기

def timer_500ms():
    red.value(red.value() ^ 1)


while True:
    time.sleep_ms(1)
    time_cnt += 1

    if time_cnt % 100 == 0:
        timer_100ms()

    if time_cnt % 500 == 0:
        timer_500ms()
