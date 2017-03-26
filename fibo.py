n = int(input())

a, b = 0,1

while n != 1:
    a, b = b, a + b
    n = n - 1

print(b)
