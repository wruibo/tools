"""
    application for security
"""
import app

if __name__ == "__main__":
    result = app.fund.analyse("HF00002H9Z", 0.014)
    #result = app.fund.analyse("1019482", 0.014)
    #result = app.fund.analyse("1000502", 0.014)
    print(result)
