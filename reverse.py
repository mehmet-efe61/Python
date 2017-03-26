def reverse_helper(l1, l2):
    if len(l1) == 0:
        return l2
    l2.append(l1.pop())
    return reverse_helper(l1, l2)

def reverse(l):
    ans = reverse_helper(l, [])
    ans2 = ans[:]
    l = reverse_helper(ans2, [])
    return ans
