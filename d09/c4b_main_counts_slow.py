from machine import Pin, Timer
import time

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False

def timer_callback(t):
    global ms_flag
    ms_flag = True  # 1ms 마다 깃발만 올린다 (세는 건 메인)

def task_100ms():
    flash.value(flash.value() ^ 1)

def task_500ms():
    red.value(red.value() ^ 1)
    time.sleep_ms(300)  # 같은 느린 일

def task_1000ms():
    global last
    now = time.ticks_ms()
    print("1초 간격 측정:", time.ticks_diff(now, last), "ms")
    last = now

last = time.ticks_ms()
tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if time_cnt % 100 == 0:
                task_100ms()
            if time_cnt % 500 == 0:
                task_500ms()
            if time_cnt % 1000 == 0:
                task_1000ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.value(0)
    red.value(1)
    print("타이머 정지")
