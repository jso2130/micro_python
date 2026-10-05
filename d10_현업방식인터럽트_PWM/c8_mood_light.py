from machine import Pin, PWM, Timer

flash = PWM(Pin(4), freq=1000, duty=0)
red = Pin(33, Pin.OUT, value=1)

# 장면 목록: (이름, 최소 밝기, 최대 밝기, 한 칸 움직이는 ms, 빨강 깜빡임 ms)
SCENES = [
    ("잔잔한 밤", 5, 120, 30, 2000),
    ("따뜻한 저녁", 20, 250, 20, 1000),
    ("설레는 파티", 30, 400, 8, 500),
]
SCENE_MS = 10000  # 장면 하나를 10초 동안 보여준다
STEPS = 100

scene = 0
level = 0
direction = 1
time_cnt = 0
ms_flag = False

def timer_callback(t):
    global ms_flag
    ms_flag = True

def level_to_duty(lv, lo, hi):
    return lo + (hi - lo) * lv * lv // (STEPS * STEPS)

def fade_step():
    global level, direction
    name, lo, hi, move_ms, blink_ms = SCENES[scene]
    level += direction
    if level >= STEPS or level <= 0:
        direction = -direction
    flash.duty(level_to_duty(level, lo, hi))

def red_blink():
    red.value(red.value() ^ 1)

def next_scene():
    global scene
    scene = (scene + 1) % len(SCENES)
    print("장면:", SCENES[scene][0])

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)
print("장면:", SCENES[scene][0])

try:
    while True:
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            if time_cnt % SCENES[scene][3] == 0:
                fade_step()

            if time_cnt % SCENES[scene][4] == 0:
                red_blink()

            if time_cnt % SCENE_MS == 0:
                next_scene()
except KeyboardInterrupt:
    tmr.deinit()
    flash.duty(0)
    flash.deinit()
    red.value(1)
    print("정지")
