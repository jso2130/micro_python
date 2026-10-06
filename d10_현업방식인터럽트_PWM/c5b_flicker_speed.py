from machine import Pin, Timer

flash = Pin(4, Pin.OUT, value=0)  # 매우 밝다, 직시 금지

PERIODS = [200, 100, 50, 20, 10]  # 한 세트의 길이(ms): 5Hz, 10Hz, 20Hz, 50Hz, 100Hz
RATIO = 30                        # 켜진 비율(%) — 모든 단계에서 같다
STAGE_MS = 4000                   # 한 단계를 4초 동안 보여 준다

time_cnt = 0
ms_flag = False
stage = -1

def timer_callback(t):
    global ms_flag
    ms_flag = True  # 1ms 마다 깃발만 올린다

tmr = Timer(0)
tmr.init(period=1, mode=Timer.PERIODIC, callback=timer_callback)

try:
    while stage < len(PERIODS):
        if ms_flag:
            ms_flag = False
            time_cnt += 1

            new_stage = time_cnt // STAGE_MS
            if new_stage != stage:
                stage = new_stage
                if stage >= len(PERIODS):
                    break
                p = PERIODS[stage]
                print("한 세트", p, "ms =", 1000 // p, "Hz — 깜빡임이 보이나요?")

            p = PERIODS[stage]
            on_time = p * RATIO // 100
            if time_cnt % p < on_time:   # 한 세트 중 앞쪽 30% 만 켠다
                flash.value(1)
            else:
                flash.value(0)
except KeyboardInterrupt:
    pass

tmr.deinit()
flash.value(0)
print("끝")
