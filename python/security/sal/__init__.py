"""
    security analyse library
"""
__all__ = ["ppa", "prr"]

# default annual days
ANNUAL_DAYS = 365

import sal.prr
import sal.ppa

# interval options
YEARLY = sal.prr.profit.YEARLY
QUARTERLY = sal.prr.profit.QUARTERLY
MONTHLY = sal.prr.profit.MONTHLY
WEEKLY = sal.prr.profit.WEEKLY
DAILY = sal.prr.profit.DAILY

# days of month, quarter, year
DAYS_OF_YEAR = sal.prr.profit.DAYS_OF_YEAR
DAYS_OF_QUARTER = sal.prr.profit.DAYS_OF_QUARTER
DAYS_OF_MONTH = sal.prr.profit.DAYS_OF_MONTH
DAYS_OF_WEEK = sal.prr.profit.DAYS_OF_WEEK
DAYS_OF_DAY = sal.prr.profit.DAYS_OF_DAY

