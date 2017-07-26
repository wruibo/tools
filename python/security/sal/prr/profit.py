"""
    compute return rate for asset/portfolio
"""
import atl, dtl

# default annual days
ANNUAL_DAYS = 365


# interval options
YEARLY = 1
QUARTERLY = 2
MONTHLY = 3
WEEKLY = 4
DAILY = 5

_support_intervals = [YEARLY, QUARTERLY, MONTHLY, WEEKLY, DAILY]

# days of month, quarter, year
DAYS_OF_YEAR = 365
DAYS_OF_QUARTER = 90
DAYS_OF_MONTH = 30
DAYS_OF_WEEK = 7
DAYS_OF_DAY = 1

# interval correspond days
_days_of_interval = {
    YEARLY:DAYS_OF_YEAR,
    QUARTERLY:DAYS_OF_QUARTER,
    MONTHLY:DAYS_OF_MONTH,
    WEEKLY:DAYS_OF_WEEK,
    DAILY:DAYS_OF_DAY
}

# interval correspond class
_cls_of_interval = {
    YEARLY:dtl.xyear,
    QUARTERLY:dtl.xquarter,
    MONTHLY:dtl.xmonth,
    WEEKLY:dtl.xweek,
    DAILY:dtl.xdate

}


def all(mtx, datecol, navcol):
    """
        compute all return rate
    :param mtx:
    :param navcol:
    :return:
    """
    results = {}

    results['total'] = total(mtx, navcol)

    results['average'] = {
        'year': average(mtx, datecol, navcol, YEARLY),
        'quarter': average(mtx, datecol, navcol, QUARTERLY),
        'month': average(mtx, datecol, navcol, MONTHLY)
    }

    results['compound'] = {
        'year': compound(mtx, datecol, navcol, YEARLY),
        'quarter': compound(mtx, datecol, navcol, QUARTERLY),
        'month': compound(mtx, datecol, navcol, MONTHLY)
    }

    results['rolling'] = {
        'year': rolling(mtx, datecol, navcol, YEARLY, ANNUAL_DAYS),
        'quarter': rolling(mtx, datecol, navcol, QUARTERLY, ANNUAL_DAYS),
        'month': rolling(mtx, datecol, navcol, MONTHLY, ANNUAL_DAYS)
    }

    results['recent'] = recent(mtx, datecol, navcol, 30, 90, 180, 360, 720, 1080, 1440, 1800)

    return results


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
    if interval is not None and interval not in _support_intervals:
        raise "invalid interval for compute average rate of return."

    # first compute the total return rate and days used for the return
    total_return_rate = total(mtx, navcol)
    total_used_days = abs(mtx[0][datecol-1] - mtx[-1][datecol-1])

    # then compute the average return rate for @interval
    avg_return_rate = total_return_rate*_days_of_interval[interval]/total_used_days

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
    if interval is not None and interval not in _support_intervals:
        raise "invalid interval for compute compound rate of return."

    # first compute the total return rate and days used for the return
    total_return_rate = total(mtx, navcol)
    total_used_days = abs(mtx[0][datecol-1] - mtx[-1][datecol-1])

    # then compute the compund return rate for @interval
    cmpd_return_rate = pow(1+total_return_rate, _days_of_interval[interval]/total_used_days) - 1

    return cmpd_return_rate


def rolling(mtx, datecol, navcol, interval=None, annualdays=None):
    """
        compute rolling return rates based on the matrix data, transform the return rates to annual if annual days specified
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :param interval: interval for compute step annual return rate
    :param annualdays: int, annual days assume for return, normally use 365 days/year
    :return: array, rate array
    """
    if interval is not None and interval not in _support_intervals:
        raise "invalid interval for compute step rate of return."

    # rolling return result, [[interval, return rate], ...]
    results = {}

    # compute the rolling return result
    if interval is None: # natural interval of the input data
        last_date, last_nav = None, None

        for row in mtx:
            curr_date, curr_nav = row[datecol-1], row[navcol-1]
            if last_date is None:
                last_date, last_nav = curr_date, curr_nav
                continue

            days = abs(curr_date-last_date)
            absrate = (curr_nav-last_nav)/last_nav

            dayrange = dtl.xrangeday(last_date, curr_date)
            annualrate = absrate*annualdays/days if annualdays is not None else absrate

            results[dayrange] = annualrate

            last_date, last_nav = curr_date, curr_nav
    else: # specified interval of the input date
        # split matrix by specified interval
        imtx = atl.matrix.split(mtx, _cls_of_interval[interval], datecol)

        # compute return of each interval, interval_return = (interval_last_nav-last_interval's_last_nav)/last_interval's_last_nav
        begin_nav = None
        for itv, navs in imtx.items():
            # get the end nav of interval
            end_nav = navs[-1][navcol-1]
            if begin_nav is None:
                begin_nav = navs[0][navcol-1]

            days = itv.days
            absrate = (end_nav-begin_nav)/begin_nav
            annualrate = absrate*annualdays/days if annualdays is not None else absrate

            results[itv] = annualrate

            # reset the begin nav value of last interval
            begin_nav = end_nav

    return results


def recent(mtx, datecol, navcol, *dayslst):
    """
        compute recent return rates based on the matrix data
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :param dayslst: tupple, recent days list want to compute return rate
    :return: array, rate array
    """
    results, today = {}, dtl.xdate()

    # compute return rate for each input days
    for days in dayslst:
        # recent begin and end date
        recent_begin_date, recent_end_date = today-days, today
        # begin & end date/nav for recent days
        begin_date, begin_nav, end_date, end_nav = None, None, None, None

        # get the begin & end date/nav from input data
        for row in mtx:
            if row[datecol-1] < recent_begin_date:
                begin_date, begin_nav = row[datecol-1], row[navcol-1]

            if row[datecol-1] >= recent_begin_date:
                end_date, end_nav = row[datecol-1], row[navcol-1]

        # compute return rate for current days
        if end_nav is not None and begin_nav is not None:
            results[days] = (end_nav-begin_nav)/begin_nav
        else:
            results[days] = None

    return results
