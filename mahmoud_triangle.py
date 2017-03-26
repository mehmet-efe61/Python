def is_triangle(x, y, z):
    return x + y > z and abs(x -y) < z

n = (input())
l = [int(x) for x in input().split()]

ans = False

#for i in range(n):
#    for j in range(i + 1, n):
#        for k in range(j + 1, n):
#            if is_triangle(l[i], l[j], l[k]):
#                ans = true

l.sort()

for i in range(n-2):
    if is_triangle(l[i], [li + 1], l[i + 2]):
        ans = True

if ans:
    print('YES')
else:
    print('NO')
