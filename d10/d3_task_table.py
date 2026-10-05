from machine import Pin, Timer

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False

def timer_callback(t):
    global ms_flag
    ms_flag = True

def task_100ms():
    flash.value(flash.value() ^ 1)

def task_500ms():
    red.value(red.value() ^ 1)

def task_1000ms():
    print("1초 경과", time_cnt)

# 주기(ms)와 할 일을 한 줄씩 적은 표
TASKS = [
    (100, task_100ms),
    (500, task_500ms),
    (1000, task_1000ms),
]

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            for period, task in TASKS:
                if time_cnt % period == 0:
                    task()
except KeyboardInterrupt:
    tmr.deinit()
    print("타이머 정지")
