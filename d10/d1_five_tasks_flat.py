from machine import Pin, Timer

flash = Pin(4, Pin.OUT, value=0)
red = Pin(33, Pin.OUT, value=1)

time_cnt = 0
ms_flag = False

def timer_callback(t):
    global ms_flag
    ms_flag = True  # 1ms 마다 깃발만 올린다

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            # 할 일이 5개 — 본문에 전부 풀어 쓴다
            if time_cnt % 10 == 0:
                pass
            if time_cnt % 50 == 0:
                pass
            if time_cnt % 100 == 0:
                flash.value(flash.value() ^ 1)
            if time_cnt % 500 == 0:
                red.value(red.value() ^ 1)
            if time_cnt % 1000 == 0:
                print("1초 경과", time_cnt)
except KeyboardInterrupt:
    tmr.deinit()
    print("타이머 정지")
