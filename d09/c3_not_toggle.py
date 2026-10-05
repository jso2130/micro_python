from machine import Pin
import time

flash = Pin(4, Pin.OUT, value=0)

print("not 0 =", not 0)
print("not 1 =", not 1)
print("처음 값:", flash.value())

for i in range(6):
    flash.value(not flash.value())  # 지금 값의 반대를 넣는다
    print(i, "번째 뒤집기 →", flash.value())
    time.sleep_ms(300)
