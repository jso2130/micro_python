print("a b | a&b  a|b  a^b  not a")
for a in (0, 1):
    for b in (0, 1):
        print(a, b, "|", a & b, "   ", a | b, "   ", a ^ b, "   ", not a)

print()
print("값 ^ 1 (XOR 토글)")
v = 0
for i in range(6):
    print(i, "번째: v =", v)
    v = v ^ 1  # 0 이면 1, 1 이면 0
