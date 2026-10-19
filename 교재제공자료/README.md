# 교재 제공자료 (출판사 `파이썬드론_제공자료_2024_11_27_1.zip` 에서 필요한 파일만)

| 폴더·파일 | 쓰임 | 교재 |
|---|---|---|
| `펌웨어/pyDrone.bin` | 드론키트 보드에 굽는 펌웨어 (1,503,632바이트, sha256 앞 16자 `0eb09e70f6991fe0`). 보드의 `0x0` 주소부터 쓴다 | 44~48쪽 |
| `라이브러리/ble_simple_peripheral.py`, `ble_advertising.py` | 블루투스 코드가 불러 쓰는 파일 두 개 — 토니에서 보드로 올린다 | 109쪽 코드의 import |
| `../d16_블루투스/3-1.블루투스통신데이터수신_1.py` | 교재 3-1 블루투스 수신 코드 (이름 `pyD_1234`) | 109~110쪽 |

## 굽기 순서 (교재 44~48쪽)
1. 프로펠러를 빼고 배터리는 연결하지 않는다. 토니의 [도구] → [옵션] → [인터프리터] → **Install or update MicroPython (esptool)**.
2. 보드의 **KEY 를 누른 채 RST 를 한 번 눌렀다 떼고 KEY 를 뗀다** (부트로더 모드).
3. 칩 `ESP32-S3`, 파일 `교재제공자료/펌웨어/pyDrone.bin` 을 고르고 설치한다 → `Wrote 1503632 bytes … Hash of data verified.`
4. **RST 를 한 번** 누르고 토니를 다시 연결한다 → 쉘에 `01Studio PYDRONE-ESP32-S3P`.

같은 일을 명령 한 줄로도 할 수 있다 (포트 이름은 컴퓨터마다 다르다):
`python -m esptool --port <포트> --baud 460800 write-flash --flash-mode dio --flash-size 8MB 0x0 pyDrone.bin`
