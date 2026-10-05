from machine import Pin, Timer

red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False
tick = 0

def timer_callback(t):
    global ms_flag
    ms_flag = True

def read_fake_sensor():
    # 가짜 센서: 0 → 100 → 0 을 오가는 값 (20초에 한 바퀴)
    return abs((tick * 10) % 200 - 100)

def task_500ms():
    red.value(red.value() ^ 1)

def task_1000ms():
    global tick
    tick += 1
    print("센서 값:", read_fake_sensor())

TASKS = [
    (500, task_500ms),
    (1000, task_1000ms),
]
CYCLE = 1000

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

            if time_cnt >= CYCLE:
                time_cnt = 0
except KeyboardInterrupt:
    tmr.deinit()
    print("타이머 정지")
