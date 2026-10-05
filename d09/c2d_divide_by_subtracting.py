number = 7                          # 나눠지는 수  (7 % 2 를 만든다)
size = 2                            # 한 번에 덜어 내는 크기
groups = 0                          # 덜어 낸 횟수 (몫)

print("시작:", number)
while number >= size:               # 덜어 낼 만큼 남아 있는 동안
    number -= size                  # 7-2, 5-2, 3-2 … 계속 뺀다
    groups += 1                     # 몇 번 뺐는지 센다
    print(number + size, "-", size, "=", number, "(", groups, "번째 )")

print("더 못 뺀다:", number, "<", size)
print("몫(뺀 횟수) =", groups)
print("나머지(남은 수) =", number)
