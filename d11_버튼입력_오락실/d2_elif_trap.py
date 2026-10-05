from machine import Pin, Timer

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False

def timer_callback(t):
    global ms_flag
    ms_flag = True

def timer_500ms():
    red.value(red.value() ^ 1)
    print("500ms", time_cnt)

def timer_1000ms():
    print("1000ms", time_cnt)

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            # 함정: 1000ms 는 500ms 의 배수이기도 하다
            if time_cnt % 1000 == 0:
                timer_1000ms()
            elif time_cnt % 500 == 0:
                timer_500ms()
except KeyboardInterrupt:
    tmr.deinit()
    print("타이머 정지")
