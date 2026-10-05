from machine import Pin, PWM, Timer

pwm = PWM(Pin(4), freq=5000, duty=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False
tick = 0
level = 0

def timer_callback(t):
    global ms_flag
    ms_flag = True

def read_fake_sensor():
    return abs((tick * 10) % 200 - 100)  # 0~100

def task_100ms():
    # 센서 값(0~100)을 밝기(0~1023)로 바꿔 플래시에 반영
    pwm.duty(level * 1023 // 100)

def task_500ms():
    red.value(red.value() ^ 1)

def task_1000ms():
    global tick, level
    tick += 1
    level = read_fake_sensor()
    print("센서 값:", level)

TASKS = [
    (100, task_100ms),
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
    pwm.deinit()
    print("타이머 정지")
