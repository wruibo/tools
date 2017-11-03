"""
    calculate total for general financial usage
"""


def interest_fixed_capital(amount, rate, periods):
    """
       calculate the captial and interest by average capital every period.
    :param amount: float, total capital amount
    :param rate: float, rate of interest per period
    :param periods: int, total periods
    :return: array, [repay period, repay capital, repay interest, repay amount, left capital]
    """
    # return capital of every period
    repay_capital = amount / periods

    # compute return capital and interest of every period
    records = []
    for i in range(periods):
        repay_period = i + 1
        repay_interest = (amount - i * repay_capital) * rate
        repay_amount = repay_capital + repay_interest
        left_capital = amount - repay_capital * repay_period
        records.append([repay_period, repay_capital, repay_interest, repay_amount, left_capital])

    return records


def interest_fixed_repayment(amount, rate, periods):
    """
        calculate the capital and interest by fixed repayment every period
    :param amount: float, total capital amount
    :param rate: float, rate of interest per period
    :param periods: int, total periods
    :return: array, [repay period, repay capital, repay interest, repay amount, left capital]
    """
    # repayment every period
    repay_amount = amount*rate*((1+rate)**periods/((1+rate)**periods-1))

    # capital repayment of first period
    first_period_repay_capital = repay_amount - amount * rate

    # compute return capital and interest of every period
    records, paid_capital = [], 0.0
    for i in range(periods):
        repay_period = i + 1
        repay_capital = first_period_repay_capital * (1 + rate)**i
        repay_interest = repay_amount - repay_capital

        paid_capital += repay_capital
        left_capital = amount -  paid_capital
        records.append([repay_period, repay_capital, repay_interest, repay_amount, left_capital])

    return records
