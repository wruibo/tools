"""
    application for security
"""
import app

if __name__ == "__main__":
    result = app.fund.analyse("HF00000G86", 0.02)
    print(result)