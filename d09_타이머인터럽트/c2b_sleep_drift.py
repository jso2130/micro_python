from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

time_cnt = 0
start = time.ticks_ms()  # 시작 시각(ms)

while time_cnt < 1000:
    time.sleep_ms(1)  # 1ms 대기
    time_cnt += 1

    if time_cnt % 100 == 0:
        flash.value(not flash.value())

spent = time.ticks_diff(time.ticks_ms(), start)
print("1ms 를 1000번 센 시간:", spent, "ms")
print("목표는 1000ms 입니다. 차이:", spent - 1000, "ms")
