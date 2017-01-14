#!/usr/bin/python
import math

# compute average of vector v
def average(v):
    return float(sum(v))/len(v)


# compute variance of vector v
def variance(v):
    sum = 0
    avg = average(v)
    for val in v:
        sum += (val-avg)**2

    return sum / (len(v)-1)

#compute standard deviation of vector v
def standard_deviation(v):
    return math.sqrt(variance(v))

#compute the covariance of vector v1 and v2
def covariance(v1, v2):
    avg1 = average(v1)
    avg2 = average(v2)

    sum = 0
    idx = num = min(len(v1),len(v2))
    while idx > 0:
        idx -= 1
        sum += (v1[idx]-avg1)*(v2[idx]-avg2)

    return sum/(num-1)

def test():
    v1 = [1,2,3,4]
    v2 = [2,3,4,5]
    print "average: ", average(v1)
    print "variance: ", variance(v1)
    print "standard deviation: ", standard_deviation(v1)
    print "conariance :", covariance(v1, v2)

test()
