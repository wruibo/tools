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

sharpeall = sharpe.all
sharpe = sharpe.sharpe

calmarall = calmar.all
calmar = calmar.calmar

betaall = beta.all
beta = beta.beta

jensenall = jensen.all
jensen = jensen.jensen

treynorall = treynor.all
treynor = treynor.treynor

sortinoall = sortino.all
sortino = sortino.sortino

inforatioall = infor.all
inforatio = infor.inforatio
