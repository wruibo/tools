"""
    security analyse library
"""
__all__ = ["ppa", "prr"]

import sal.prr
import sal.ppa

# default annual days
ANNUAL_DAYS = sal.prr.profit.ANNUAL_DAYS


# interval options
YEARLY = sal.prr.profit.YEARLY
QUARTERLY = sal.prr.profit.QUARTERLY
MONTHLY = sal.prr.profit.MONTHLY
DAILY = sal.prr.profit.DAILY

# days of month, quarter, year
DAYS_OF_MONTH = sal.prr.profit.DAYS_OF_MONTH
DAYS_OF_QUARTER = sal.prr.profit.DAYS_OF_QUARTER
DAYS_OF_YEAR = sal.prr.profit.DAYS_OF_YEAR
DAYS_OF_DAY = sal.prr.profit.DAYS_OF_DAY


