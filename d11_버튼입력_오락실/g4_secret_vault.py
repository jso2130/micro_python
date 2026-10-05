from machine import Pin, PWM, Timer
import time

btn = Pin(0, Pin.IN, Pin.PULL_UP)               # 누르면 0
flash = PWM(Pin(4), freq=1000, duty=0)          # 플래시 (직시 금지)
red = Pin(33, Pin.OUT, value=1)                 # 0 이 켜짐

SHORT = "짧"
LONG = "긴"
PATTERN = [SHORT, SHORT, LONG]   # 비밀번호: 여기만 바꾸면 된다 (예: [LONG, SHORT, LONG, SHORT])
LONG_MS = 500                    # 이 시간 이상 누르면 "긴"
INPUT_TIMEOUT_MS = 3000          # 이 시간 동안 입력이 없으면 처음부터
OPEN_DUTY = 700                  # 열렸을 때 최대 밝기
OPEN_STEP = 5                    # 10ms 마다 밝아지는 크기
OPEN_HOLD = 300                  # 열린 채 유지하는 시간 (10ms 단위, 300 = 3초)

LOCKED = 0
OPENING = 1
OPENED = 2
CLOSING = 3
DENIED = 4

state = LOCKED
entered = []             # 지금까지 입력한 패턴
duty = 0
hold_cnt = 0
deny_cnt = 0
press_start = 0
last_input = 0
btn_last = 1

flag_10ms = False
flag_100ms = False
isr_cnt = 0

def timer_isr(t):
    global isr_cnt, flag_10ms, flag_100ms
    isr_cnt += 1
    if isr_cnt % 10 == 0:
        flag_10ms = True
    if isr_cnt % 100 == 0:
        flag_100ms = True
    if isr_cnt >= 1000:
        isr_cnt = 0

def on_release(held):
    global state, entered, last_input, deny_cnt
    kind = LONG if held >= LONG_MS else SHORT
    entered.append(kind)
    last_input = time.ticks_ms()
    print("입력", len(entered), "번째:", kind, "(", held, "ms )")
    if entered[-1] != PATTERN[len(entered) - 1]:   # 틀렸다
        print("틀렸습니다! 경고")
        entered = []
        deny_cnt = 0
        state = DENIED
    elif len(entered) == len(PATTERN):             # 끝까지 맞았다
        print("열림!")
        entered = []
        state = OPENING

def task_10ms():
    global btn_last, press_start, state, duty, hold_cnt, entered
    now = btn.value()
    if state == LOCKED:
        red.value(now)                             # 누르는 동안 빨간 LED 가 따라 켜진다
        if btn_last == 1 and now == 0:
            press_start = time.ticks_ms()
        elif btn_last == 0 and now == 1:
            on_release(time.ticks_diff(time.ticks_ms(), press_start))
        elif entered and now == 1 and time.ticks_diff(time.ticks_ms(), last_input) >= INPUT_TIMEOUT_MS:
            entered = []                           # 한참 입력이 없으면 처음부터
            print("시간 초과, 처음부터")
    elif state == OPENING:                         # 서서히 켜진다
        duty += OPEN_STEP
        if duty >= OPEN_DUTY:
            duty = OPEN_DUTY
            hold_cnt = 0
            state = OPENED
        flash.duty(duty)
    elif state == OPENED:                          # 잠시 열린 채 유지
        hold_cnt += 1
        if hold_cnt >= OPEN_HOLD:
            state = CLOSING
    elif state == CLOSING:                         # 서서히 꺼지고 다시 잠긴다
        duty -= OPEN_STEP
        if duty <= 0:
            duty = 0
            state = LOCKED
            red.value(1)
            print("다시 잠김")
        flash.duty(duty)
    btn_last = now

def task_100ms():
    global state, deny_cnt
    if state == DENIED:
        red.value(red.value() ^ 1)                 # 빨간 LED 경고 깜빡
        deny_cnt += 1
        if deny_cnt >= 12:
            red.value(1)
            state = LOCKED
            print("다시 입력하세요")

TASKS = [
    (10, task_10ms),
    (100, task_100ms),
]

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)
print("비밀 금고! 패턴:", PATTERN)

try:
    while True:
        if flag_10ms:
            flag_10ms = False
            task_10ms()
        if flag_100ms:
            flag_100ms = False
            task_100ms()
except KeyboardInterrupt:
    tmr.deinit()
    flash.duty(0)
    flash.deinit()
    red.value(1)
    print("정지")

# ⭐ 도전: 3번 연속 틀리면 10초 동안 잠기게 만들어 보자. 패턴을 4개로 늘리면 더 어려워진다.
