"""
    compute return rate for asset/portfolio
"""
import utl

# default annual days
ANNUAL_DAYS = 365


# interval options
YEARLY = 1
QUARTERLY = 2
MONTHLY = 3
DAILY = 4

# days of month, quarter, year
DAYS_OF_YEAR = 365
DAYS_OF_QUARTER = 90
DAYS_OF_MONTH = 30
DAYS_OF_DAY = 1

_interval_days = {
    YEARLY:DAYS_OF_YEAR,
    QUARTERLY:DAYS_OF_QUARTER,
    MONTHLY:DAYS_OF_MONTH,
    DAILY:DAYS_OF_DAY
}

def all(mtx, navcol):
    """
        compute all return rate
    :param mtx:
    :param navcol:
    :return:
    """
    pass


def total(mtx, navcol):
    """
        compute total return rate
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :return: float, total profix
    """
    return (mtx[-1][navcol-1]-mtx[0][navcol-1]) / mtx[0][navcol-1]


def average(mtx, datecol, navcol, interval=None):
    """
        compute average @interval return rate
    :param mtx: matrix,
    :param datecol: int, date column start from 1
    :param navcol: int, nav column start from 1
    :param interval: int, values in [YEARLY, QUARTERLY, MONTHLY, DAILY]
    :return: float, average return rate measure by @interval
    """
    if interval is not None and interval not in _interval_days.keys():
        raise "invalid interval for compute average rate of return."

    # first compute the total return rate and days used for the return
    total_return_rate = total(mtx, navcol)
    total_used_days = abs(mtx[0][datecol-1] - mtx[-1][datecol-1])

    # then compute the average return rate for @interval
    avg_return_rate = total_return_rate*_interval_days[interval]/total_used_days

    return avg_return_rate


def compound(mtx, datecol, navcol, interval=None):
    """
        compute compound @interval return rate
    :param mtx: matrix,
    :param datecol: int, date column start from 1
    :param navcol: int, nav column start from 1
    :param interval: int, values in [YEARLY, QUARTERLY, MONTHLY, DAILY]
    :return: float, compound return rate measure by @interval
    """
    if interval is not None and interval not in _interval_days.keys():
        raise "invalid interval for compute compound rate of return."

    # first compute the total return rate and days used for the return
    total_return_rate = total(mtx, navcol)
    total_used_days = abs(mtx[0][datecol-1] - mtx[-1][datecol-1])

    # then compute the compund return rate for @interval
    cmpd_return_rate = pow(1+total_return_rate, _interval_days[interval]/total_used_days) - 1

    return cmpd_return_rate


def annuals(mtx, navcol):
    pass


def quarters(mtx, navcol):
    pass


def months(mtx, navcol):
    pass


def roll(mtx, datecol, navcol, interval=None, annualdays=None):
    pass


def step(mtx, datecol, navcol, interval=None, annualdays=None):
    """
        compute step(interval) return rates based on the matrix data
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :param interval: interval for compute step annual return rate
    :param annualdays: int, annual days assume for return, normally use 365 days/year
    :return: array, rate array
    """
    if interval is not None and interval not in _interval_days.keys():
        raise "invalid interval for compute step rate of return."

    if interval is None:
        period_rates, last_date, last_nav = [], None, None

        for row in mtx:
            curr_date, curr_nav = row[datecol-1], row[navcol-1]
            if last_date is None:
                last_date, last_nav = curr_date, curr_nav
                continue

            days = abs(curr_date-last_date)
            rate = (curr_nav-last_nav)/last_nav

            period_rate = rate*annualdays/days if annualdays is not None else rate/days
            period_rates.append(period_rate)

            last_date, last_nav = curr_date, curr_nav

        return period_rates
    else:
        utl.date.years_between()
