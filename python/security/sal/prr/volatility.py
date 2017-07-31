
AB2 = [0.5, 0.6, 0.95, 2, 2, 2.05]

B = AB2

#B = [0.05,  0.2 ,  0.9 ,  3.  ,  3.  ,  3.]
BBB = []

largethan1 = 0
lessthan02 = 0
lessthan0204 = 0
sum = 0.0

rate = 0.0

i, j, k = 0, 0, 0
for b1 in B:
    BBB.append([])
    for b2 in B:
        BBB[i].append([])
        for b3 in B:
            BBB[i][j].append([])
            for b4 in B:
                BBB[i][j][k].append(b1*b2*b3*b4)
                sum += b1*b2*b3*b4
                if b1*b2*b3*b4>1.0:
                    largethan1 += 1
                if b1 * b2 * b3 * b4 < 0.2:
                    lessthan02 +=1

                if b1 * b2 * b3 * b4 >= 2.4 and b1*b2*b3*b4<2.6:
                    lessthan0204 += 1

            k += 1
        j += 1
        k = 0
    i += 1
    j = 0
    k = 0

print(BBB)

print(largethan1)
print(sum)
print(sum/1296)
print(lessthan02)
print(lessthan0204)
print(lessthan0204/1296)

def mrandom(arr, times):
    pass


