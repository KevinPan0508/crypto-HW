def fab(n):
    list = [0] * n
    list[0] = 1
    list[1] = 1
    for i in range(2,n):
        list[i] = list[i-1] + list[i-2]
    return list