"""
    application for security
"""
import app

if __name__ == "__main__":
    app.fund.source(app.fund.vendor.cfq)
    #result = app.fund.analyse("HF00002H9Z", 0.014)
    #result = app.fund.analyse("HF000011M7", 0.014)
    #result = app.fund.analyse("HF00000STD", 0.014)

    #result = app.fund.analyse("1019482", 0.014)
    #result = app.fund.analyse("1005096", 0.014)
    #result = app.fund.analyse("1025925", 0.014)
    #result = app.fund.analyse("1000143", 0.014)
    #result = app.fund.analyse("1042823", 0.014)
    result = app.fund.analyse("1042823", 0.014)
    print(result)

