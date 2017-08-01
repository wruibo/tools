"""
    compute return rate for asset/portfolio
"""
import atl, dtl


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
        'year': average(mtx, datecol, navcol, dtl.xyear),
        'quarter': average(mtx, datecol, navcol, dtl.xquarter),
        'month': average(mtx, datecol, navcol, dtl.xmonth),
        'week': average(mtx, datecol, navcol, dtl.xweek)
    }

    results['compound'] = {
        'year': compound(mtx, datecol, navcol, dtl.xyear),
        'quarter': compound(mtx, datecol, navcol, dtl.xquarter),
        'month': compound(mtx, datecol, navcol, dtl.xmonth),
        'week': compound(mtx, datecol, navcol, dtl.xweek)
    }

    results['rolling'] = {
        'year': rolling(mtx, datecol, navcol, dtl.xyear),
        'quarter': rolling(mtx, datecol, navcol, dtl.xquarter),
        'month': rolling(mtx, datecol, navcol, dtl.xmonth),
        'week': rolling(mtx, datecol, navcol, dtl.xweek)
    }

    results['recent'] = {
        'year': recent(mtx, datecol, navcol, dtl.xyear),
        'quarter': recent(mtx, datecol, navcol, dtl.xquarter),
        'month': recent(mtx, datecol, navcol, dtl.xmonth),
        'week': recent(mtx, datecol, navcol, dtl.xweek)
    }

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


def average(mtx, datecol, navcol, periodcls):
    """
        compute average return rate by specified period
    :param mtx: matrix,
    :param datecol: int, date column start from 1
    :param navcol: int, nav column start from 1
    :param periodcls: class, period want to compute average return rate
    :return: float, average return rate measure by specified period
    """
    if issubclass(periodcls, dtl.xperiod):
        raise "invalid period for compute average return rate."

    # first compute the total return rate and days used for the return
    total_return_rate = total(mtx, navcol)
    total_used_days = abs(mtx[0][datecol-1] - mtx[-1][datecol-1])

    # then compute the average return rate by specified period
    avg_return_rate = total_return_rate*periodcls.unitdays()/total_used_days

    return avg_return_rate


def compound(mtx, datecol, navcol, periodcls):
    """
        compute compound return rate by specified period
    :param mtx: matrix,
    :param datecol: int, date column start from 1
    :param navcol: int, nav column start from 1
    :param periodcls: class, period want to compute compound return rate
    :return: float, compound return rate measure by specified period
    """
    if issubclass(periodcls, dtl.xperiod):
        raise "invalid period for compute compound return rate."

    # first compute the total return rate and days used for the return
    total_return_rate = total(mtx, navcol)
    total_used_days = abs(mtx[0][datecol-1] - mtx[-1][datecol-1])

    # then compute the compund return rate by specified period
    cmpd_return_rate = pow(1+total_return_rate, periodcls.unitdays()/total_used_days) - 1

    return cmpd_return_rate


def rolling(mtx, datecol, navcol, periodcls=None, annualdays=None):
    """
        compute rolling return rates by specified rolling period
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :param periodcls: class, rolling period
    :param annualdays: int, annual days assume for return, normally use 365 days/year
    :return: array, rate array
    """
    if issubclass(periodcls, dtl.xperiod):
        raise "invalid period for compute rolling return rates."

    # rolling return result, [[period, return rate], ...]
    results = {}

    # compute the rolling return result
    if periodcls is None: # natural period of the input data
        last_date, last_nav = None, None

        for row in mtx:
            curr_date, curr_nav = row[datecol-1], row[navcol-1]
            if last_date is None:
                last_date, last_nav = curr_date, curr_nav
                continue

            days = abs(curr_date-last_date)
            absrate = (curr_nav-last_nav)/last_nav

            dayrange = dtl.xrangeday(last_date, curr_date)
            annualrate = pow(1+absrate, annualdays/days)-1 if annualdays is not None else absrate

            results[dayrange] = annualrate

            last_date, last_nav = curr_date, curr_nav
    else: # specified period of the input date
        # split matrix by specified period
        pmtx = atl.matrix.split(mtx, periodcls, datecol)

        # compute return of each period, period_return = (period_last_nav-last_period's_last_nav)/last_period's_last_nav
        begin_nav = None
        for prd, navs in pmtx.items():
            # get the end nav of period
            end_nav = navs[-1][navcol-1]
            if begin_nav is None:
                begin_nav = navs[0][navcol-1]

            days = prd.days
            absrate = (end_nav-begin_nav)/begin_nav
            annualrate = pow(1+absrate, annualdays/days)-1 if annualdays is not None else absrate

            results[prd] = annualrate

            # reset the begin nav value of last period
            begin_nav = end_nav

    return results


def recent(mtx, datecol, navcol, periodcls, periods=1, annualdays=None):
    """
        compute recent return rates based on the matrix data
    :param mtx: matrix
    :param datecol: int, date column in matrix
    :param navcol: int, nav column in matrix
    :param periodcls: class, recent period
    :param periods: int, number of period
    :param annualdays: int, annual days assume for return, normally use 365 days/year
    :return: dict, rate array
    """
    # today
    today = dtl.xdate()

    # recent begin and end date
    recent_begin_date = today.back(periodcls, periods)
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
        absrate = (end_nav-begin_nav)/begin_nav
        return pow(1+absrate, annualdays/(periods*periodcls.unitdays())) - 1 if annualdays is not None else absrate
    else:
        return None
