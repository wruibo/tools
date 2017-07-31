"""
    portfolio construction algorithm
"""
import atl, math


def simulate(navs, times, stepval=0.2):
    # navs after invested times
    navs_after_invest_times = atl.array.pmrcombine(*[navs for i in range(0, times)])

    # steps for statistic
    total = len(navs_after_invest_times)
    steps = math.ceil(max(navs_after_invest_times)/stepval)+1

    # statistic for distribution of returns
    dists = [0 for i in range(0, steps)]
    for nav in navs_after_invest_times:
        pos = math.floor(nav/stepval)
        dists[pos] = dists[pos] + 1


    # probability distribution for returns
    results = []
    for cnt in dists:
        results.append(cnt/total)

    return results



if __name__ == "__main__":
    navsA = [0.05, 0.2, 1, 3, 3, 3]
    navsB = [0.8, 0.9, 1.1, 1.1, 1.2, 1.4]
    navsC = [0.95, 1, 1, 1, 1, 1.1]

    navsAB = atl.array.divide(atl.array.add(navsA, navsB), 2)
    navsAC = atl.array.divide(atl.array.add(navsA, navsC), 2)
    navsBC = atl.array.divide(atl.array.add(navsB, navsC), 2)


    times, stepval = 5, 0.2

    resA = simulate(navsA, times, stepval)
    resB = simulate(navsB, times, stepval)
    resC = simulate(navsC, times, stepval)

    resAB = simulate(navsAB, times, stepval)
    resAC = simulate(navsAC, times, stepval)
    resBC = simulate(navsBC, times, stepval)

    import matplotlib.pyplot as plt

    plt.figure(figsize=(16, 8))
    plt.xlabel("invest times(%d), step by(%s)" % (times, str(stepval)))
    plt.ylabel("return rates")
    plt.plot(resA, label="$A%s$"%str(navsA))
    plt.plot(resB, label="$B%s$"%str(navsB))
    plt.plot(resC, label="$C%s$"%str(navsC))
    plt.plot(resAB, label="$AB%s$" % str(navsAB))
    plt.plot(resAC, label="$AC%s$" % str(navsAC))
    plt.plot(resBC, label="$BC%s$" % str(navsBC))

    plt.legend()
    plt.show()
