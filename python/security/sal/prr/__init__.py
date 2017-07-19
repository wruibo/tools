"""
    portfolio risk & return analyse
"""
__all__ = ["profit", "mdd", "beta", "jensen", "sharpe", "treynor"]

import sal.prr.profit
import sal.prr.mdd
import sal.prr.beta
import sal.prr.jensen
import sal.prr.sharpe
import sal.prr.treynor
import sal.prr.infor
import sal.prr.calmar
import sal.prr.sortino

sharpe = sharpe.sharpe
calmar = calmar.calmar
beta = beta.beta
jensen = jensen.jensen
treynor = treynor.treynor
sortino = sortino.sortino
inforatio = infor.inforatio