"""
    application for security
"""
import app, utl, dbm

if __name__ == "__main__":
    result = app.fund.analyse("HF00002H9Z", 0.014)
    #result = app.fund.analyse("HF000011M7", 0.014)
    #result = app.fund.analyse("HF00000STD", 0.014)

    #result = app.fund.analyse("1019482", 0.014)
    #result = app.fund.analyse("1005096", 0.014)
    #result = app.fund.analyse("1025925", 0.014)
    #result = app.fund.analyse("1000143", 0.014)
    #result = app.fund.analyse("1000502", 0.014)
    print(result)
    arr1 = [1, 2, [3, 2], 1]
    arr2 = [1, 2, [3, 3.0], 1]

    print(utl.math.array.like(arr1, arr2))
    print(utl.math.array.similar(arr1, arr2))
