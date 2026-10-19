# 교재 제공자료 (출판사 `파이썬드론_제공자료_2024_11_27_1.zip` 에서 필요한 파일만)

| 폴더·파일 | 쓰임 | 교재 |
|---|---|---|
| `펌웨어/pyDrone.bin` | 드론키트 보드에 굽는 펌웨어 (1,503,632바이트, sha256 앞 16자 `0eb09e70f6991fe0`). 보드의 `0x0` 주소부터 쓴다 | 44~48쪽 |
| `라이브러리/ble_simple_peripheral.py`, `ble_advertising.py` | 블루투스 코드가 불러 쓰는 파일 두 개 — 토니에서 보드로 올린다 | 109쪽 코드의 import |
| `../d16_블루투스/3-1.블루투스통신데이터수신_1.py` | 교재 3-1 블루투스 수신 코드 (이름 `pyD_1234`) | 109~110쪽 |

## 펌웨어 설치 순서 (교재 44~48쪽, 토니 사용)
1. 프로펠러를 빼고 배터리는 연결하지 않는다. 토니 [도구] → [옵션] → **인터프리터** 탭 → 오른쪽 아래 **Install or update MicroPython (esptool)** 을 누른다.
2. 보드의 **RST 와 KEY 를 함께 눌렀다가 RST 를 먼저, KEY 를 나중에 뗀다** (부트모드).
3. 설치 창에서 **Target port** `USB JTAG/serial debug unit`, **MicroPython family** `ESP32-S3`, **≡ → Select local MicroPython image…** 로 `펌웨어/pyDrone.bin` 을 고른다.
4. variant `<local file>` · version `pyDrone.bin` 을 확인하고 **[설치]** → `Done!` 이 나오면 **[닫기]**.
5. 보드의 **RST** 를 한 번 누른다. 토니 **오른쪽 아래에서 `MicroPython (ESP32) · Espressif Device @ 내 포트`** 를 선택하고 **STOP** 을 한 번 누른다 → 쉘에 `01Studio PYDRONE-ESP32-S3P` 와 `>>>`.
