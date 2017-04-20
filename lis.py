import math

ar = [int(x) for x in input().split()]

lis = [-math.inf] * (len(ar) + 1)
n = 0

for x in ar:
    lo, hi = 0, n

    while lo < hi:
        md = (lo + hi) // 2 + 1
        if lis[md] <= x:
            lo = md
        else:
            hi = md - 1
    
    lis[lo + 1] = x
    n = max(n, lo + 1)

print(n)
