from machine import Pin, PWM, Timer
import time
import random

btn = Pin(0, Pin.IN, Pin.PULL_UP)               # 누르면 0
flash = PWM(Pin(4), freq=1000, duty=0)          # 플래시 (직시 금지)
red = Pin(33, Pin.OUT, value=1)                 # 0 이 켜짐

# ---- 조작 규칙 ----
# 메뉴에서: 짧게 클릭 = 다음 모드 / 1초 이상 꾹 = 이 모드 시작
#          (빨간 LED 가 모드 번호만큼 깜빡: 1=손전등 2=호흡등 3=반응속도 4=금고)
# 게임 중에: 3초 이상 꾹 = 메뉴로 돌아가기
MODE_NAMES = ["손전등", "호흡등", "반응속도", "금고"]
HOLD_START_MS = 1000
EXIT_MS = 3000
LONG_MS = 500

mode = 0              # 0~3
in_menu = True
btn_last = 1
press_start = 0
ignore_release = False   # 꾹 눌러 모드가 바뀐 뒤, 떼는 동작은 무시
blink_phase = 0

# ---- 모드 1: 손전등 ----
LEVELS = [0, 60, 250, 700]
lamp_state = 0

# ---- 모드 2: 호흡등(디머) ----
MIN_DUTY = 20
MAX_DUTY = 700
FADE_STEP = 8
dim_level = 300
dim_on = False
dim_dir = 1
dim_long = False

# ---- 모드 3: 반응속도 ----
IDLE = 0
READY = 1
GO = 2
FOUL = 3
rx_state = IDLE
rx_wait = 0
rx_t0 = 0
rx_best = None
rx_foul = 0

# ---- 모드 4: 금고 ----
SHORT = "짧"
LONG = "긴"
PATTERN = [SHORT, SHORT, LONG]
v_entered = []
v_state = 0           # 0 잠김, 1 열리는 중, 2 열림 유지, 3 닫히는 중, 4 경고
v_duty = 0
v_hold = 0
v_deny = 0
v_last = 0

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

def nothing(*args):
    pass

def reset_outputs():
    flash.duty(0)
    red.value(1)

# ================= 모드 1: 손전등 =================
def lamp_init():
    global lamp_state
    lamp_state = 0

def lamp_press():
    global lamp_state
    lamp_state = (lamp_state + 1) % len(LEVELS)
    flash.duty(LEVELS[lamp_state])
    red.value(0 if lamp_state > 0 else 1)
    print("손전등 단계", lamp_state)

# ================= 모드 2: 호흡등 =================
def dim_apply():
    flash.duty(dim_level if dim_on else 0)
    red.value(0 if dim_on else 1)

def dim_init():
    global dim_on, dim_long
    dim_on = False
    dim_long = False

def dim_press():
    global dim_long
    dim_long = False

def dim_hold(held):
    global dim_long, dim_on, dim_level, dim_dir
    if held >= LONG_MS:
        if not dim_long:
            dim_long = True
            dim_on = True
        dim_level += FADE_STEP * dim_dir
        if dim_level >= MAX_DUTY:
            dim_level = MAX_DUTY
            dim_dir = -1
        if dim_level <= MIN_DUTY:
            dim_level = MIN_DUTY
            dim_dir = 1
        dim_apply()

def dim_release(held):
    global dim_on, dim_dir
    if dim_long:
        dim_dir = -dim_dir
        print("호흡등 고정", dim_level)
    else:
        dim_on = not dim_on
        dim_apply()
        print("호흡등", "켜짐" if dim_on else "꺼짐")

# ================= 모드 3: 반응속도 =================
def rx_init():
    global rx_state
    rx_state = IDLE
    print("반응속도: 버튼을 누르면 시작")

def rx_press():
    global rx_state, rx_wait, rx_t0, rx_best, rx_foul
    if rx_state == IDLE:
        random.seed(time.ticks_ms())
        rx_wait = random.randint(1000, 4000)
        rx_t0 = time.ticks_ms()
        red.value(0)
        rx_state = READY
        print("준비...")
    elif rx_state == READY:
        rx_foul = 0
        rx_state = FOUL
        print("반칙!")
    elif rx_state == GO:
        rt = time.ticks_diff(time.ticks_ms(), rx_t0)
        print("반응 시간:", rt, "ms")
        if rx_best is None or rt < rx_best:
            rx_best = rt
            print("★ 최고 기록 갱신!", rx_best, "ms")
        flash.duty(0)
        rx_state = IDLE

def rx_10ms():
    global rx_state, rx_t0
    if rx_state == READY and time.ticks_diff(time.ticks_ms(), rx_t0) >= rx_wait:
        flash.duty(600)
        red.value(1)
        rx_t0 = time.ticks_ms()
        rx_state = GO
    elif rx_state == GO and time.ticks_diff(time.ticks_ms(), rx_t0) >= 3000:
        flash.duty(0)
        rx_state = IDLE
        print("너무 느려요")

def rx_100ms():
    global rx_state, rx_foul
    if rx_state == FOUL:
        red.value(red.value() ^ 1)
        rx_foul += 1
        if rx_foul >= 12:
            red.value(1)
            rx_state = IDLE

# ================= 모드 4: 금고 =================
def vault_init():
    global v_entered, v_state, v_duty
    v_entered = []
    v_state = 0
    v_duty = 0
    print("금고 패턴:", PATTERN)

def vault_release(held):
    global v_entered, v_state, v_deny, v_last
    if v_state != 0:
        return
    kind = LONG if held >= LONG_MS else SHORT
    v_entered.append(kind)
    v_last = time.ticks_ms()
    print("입력", len(v_entered), kind)
    if v_entered[-1] != PATTERN[len(v_entered) - 1]:
        print("틀렸습니다!")
        v_entered = []
        v_deny = 0
        v_state = 4
    elif len(v_entered) == len(PATTERN):
        print("열림!")
        v_entered = []
        v_state = 1

def vault_10ms():
    global v_state, v_duty, v_hold, v_entered
    if v_state == 0:
        red.value(btn.value())
        if v_entered and btn.value() == 1 and time.ticks_diff(time.ticks_ms(), v_last) >= 3000:
            v_entered = []
            print("시간 초과, 처음부터")
    elif v_state == 1:
        v_duty += 5
        if v_duty >= 700:
            v_duty = 700
            v_hold = 0
            v_state = 2
        flash.duty(v_duty)
    elif v_state == 2:
        v_hold += 1
        if v_hold >= 300:
            v_state = 3
    elif v_state == 3:
        v_duty -= 5
        if v_duty <= 0:
            v_duty = 0
            v_state = 0
            red.value(1)
        flash.duty(v_duty)

def vault_100ms():
    global v_state, v_deny
    if v_state == 4:
        red.value(red.value() ^ 1)
        v_deny += 1
        if v_deny >= 12:
            red.value(1)
            v_state = 0

# ---- 모드별 함수를 번호 순서로 묶은 표 ----
INITS = [lamp_init, dim_init, rx_init, vault_init]
ON_PRESS = [lamp_press, dim_press, rx_press, nothing]
ON_HOLD = [nothing, dim_hold, nothing, nothing]
ON_RELEASE = [nothing, dim_release, nothing, vault_release]
ON_10MS = [nothing, nothing, rx_10ms, vault_10ms]
ON_100MS = [nothing, nothing, rx_100ms, vault_100ms]

# ================= 메뉴 =================
def enter_mode():
    global in_menu
    in_menu = False
    reset_outputs()
    INITS[mode]()
    print("모드 시작:", MODE_NAMES[mode])

def go_menu():
    global in_menu, blink_phase
    in_menu = True
    blink_phase = 0
    reset_outputs()
    print("메뉴로 돌아옴. 현재 선택:", mode + 1, MODE_NAMES[mode])

def menu_100ms():
    global blink_phase
    n = mode + 1                              # 모드 번호만큼 깜빡
    if blink_phase < n * 2:
        red.value(blink_phase % 2)            # 짝수 단계에서 켜짐(0)
    else:
        red.value(1)                          # 쉬는 시간
    blink_phase = (blink_phase + 1) % (n * 2 + 8)

def task_10ms():
    global btn_last, press_start, ignore_release, mode, blink_phase
    now = btn.value()
    if btn_last == 1 and now == 0:                    # 막 눌렀다
        press_start = time.ticks_ms()
        ignore_release = False
        if not in_menu:
            ON_PRESS[mode]()
    elif now == 0 and not ignore_release:             # 누르고 있는 중
        held = time.ticks_diff(time.ticks_ms(), press_start)
        if in_menu:
            if held >= HOLD_START_MS:
                enter_mode()
                ignore_release = True
        elif held >= EXIT_MS:
            go_menu()
            ignore_release = True
        else:
            ON_HOLD[mode](held)
    elif btn_last == 0 and now == 1:                  # 막 뗐다
        held = time.ticks_diff(time.ticks_ms(), press_start)
        if ignore_release:
            ignore_release = False
        elif in_menu:                                 # 짧은 클릭 = 다음 모드
            mode = (mode + 1) % len(MODE_NAMES)
            blink_phase = 0
            print("선택:", mode + 1, MODE_NAMES[mode])
        else:
            ON_RELEASE[mode](held)
    btn_last = now
    if not in_menu:
        ON_10MS[mode]()

def task_100ms():
    if in_menu:
        menu_100ms()
    else:
        ON_100MS[mode]()

TASKS = [
    (10, task_10ms),
    (100, task_100ms),
]

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_isr)
print("오락실! 클릭=다음 모드, 1초 꾹=시작, 3초 꾹=메뉴")

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

# ⭐ 도전: 새 모드(예: SOS 신호등)를 하나 추가해 보자. 표(INITS, ON_PRESS...)에 한 칸씩만 넣으면 된다.
