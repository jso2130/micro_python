"""BLE 로 받은 바이트를 그대로 쉘에 찍기
미확인: 광고 이름이 폰에 보이는 모습, 쉘의 bytes 모양(직접 확인)"""
import bluetooth, ble_simple_peripheral

NAME = "pyD_00"                      # ★ 내 번호로

ble = bluetooth.BLE()
p = ble_simple_peripheral.BLESimplePeripheral(ble, name=NAME)


def on_rx(read):                     # 폰이 값을 써 넣으면 불린다
    print("받음:", read, "길이", len(read))


p.on_write(on_rx)
print("광고 중:", NAME)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("정지")
