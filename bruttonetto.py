#!/usr/bin/env python2
#  https://www.sthu.org/blog/02-bruttonetto/index.html
__author__ = "Stefan Huber"
__copyright__ = "Copyright 2013"

__version__ = "1.0"
__license__ = "LGPL3"


import sys, getopt, os

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def uiPerMonth(gross):
    """Returns unemployment insurance rates (in percent) from a specific gross
    income per month."""
    if gross <= 1219:
        return 0.0
    elif gross <= 1330:
        return 1.0
    elif gross <= 1497:
        return 2.0
    else:
        return 3.0

def siPerMonth(month, gross):
    """Returns social insurance dues from a specific gross income per month for
    the given month. Month is between 1 and 14."""

    if gross <= 386.80:
        return 0

    # retirement pension insurance, health insurance, unemployment insurace
    rates = 10.25 + 3.82 + uiPerMonth(gross)
    if month <= 12:
        # chamber of labour dues, residential building support
        rates += 0.5 + 0.5

    return rates/100.0 * min(gross, 4400)

def incometax(ref):
    """Income tax of the reference (gross per year minus reductions)."""

    if ref > 60000:
        return (ref-60000)*0.5 + incometax(60000)
    elif ref > 25000:
        return (ref-25000)*0.43214286 + incometax(25000)
    elif ref > 11000:
        return (ref-11000)*0.365 + incometax(11000)
    else:
        return 0

def itertable(ref):
    """Returns the income tax of the reference (gross minus reductions)
    according to the effective rates table (Effektiv-Tarif-Tabelle)."""

    net = None

    if ref <= 1011.43:
        net = 0.0
    elif ref <= 2099.33:
        net = ref * 0.365 - 369.173
    elif ref <= 5016:
        net = ref * 0.4321429 - 510.129
    else:
        net = ref * 0.5 - 850.5

    return net

def itPerMonth(month, gross):
    """Returns income tax from a specific gross income per month for the given
    month. Month is between 1 and 14."""

    # The reference value for the income tax
    ref = gross - siPerMonth(month, gross)

    if month > 12:
        # Reduction of taxes for special renumeration
        if month == 13:
            ref -= 620

        # The number 1050 was reverse engineegreen from "Brutto-Netto-Rechner"
        # from the webpage of the ministry of finance.
        if gross <= 1050:
            return 0
        else:
            return ref * 6.0/100.0
    else:
        return itertable(ref);

def netPerMonth(month, gross):
    """Returns net income from a specific gross income per month for the given
    month. Month is between 1 and 14."""
    return gross - siPerMonth(month, gross) - itPerMonth(month, gross)

def netPerYear(gross):
    """Returns net income per year of given per-month gross income."""
    return sum([netPerMonth(m, gross) for m in range(1, 15)])

def itPerYear(gross):
    """Returns income tax per year of given per-month gross income."""
    return sum([itPerMonth(m, gross) for m in range(1, 15)])

def siPerYear(gross):
    """Returns socual insurance tax per year of given per-month gross income."""
    return sum([siPerMonth(m, gross) for m in range(1, 15)])


def printTaxesTable(gross):
    """Print a table with taxes for given per-month gross income."""

    print("          |  1.-12. month |  13. month |  14. month ||       year")
    print("          |---------------+------------+------------++------------")
    print("gross     | %13.2f | %10.2f | %10.2f || %10.2f" % \
            (gross, gross, gross, 14*gross))
    print("          |---------------+------------+------------++------------")
    print("soc. ins. | %13.2f | %10.2f | %10.2f || %10.2f" % \
            (siPerMonth(1, gross),
                siPerMonth(13, gross),
                siPerMonth(14, gross),
                siPerYear(gross)))
    print("inc. tax  | %13.2f | %10.2f | %10.2f || %10.2f" % \
            (itPerMonth(1, gross),
                itPerMonth(13, gross),
                itPerMonth(14, gross),
                itPerYear(gross)))
    print("          |---------------+------------+------------++------------")
    print("net       | %13.2f | %10.2f | %10.2f || %10.2f" % \
            (netPerMonth(1, gross),
                netPerMonth(13, gross),
                netPerMonth(14, gross),
                netPerYear(gross)))

def diffQuotient(func, delta=1.0):
    return lambda x: (func(x+delta) - func(x))/delta


def showPlots():

    print("Showing plots...")


    plt.figure(1, figsize=(6.5, 8), dpi=80, facecolor='w')
    plt.subplots_adjust(left=0.13, right=0.95, bottom=0.06, top=0.98)
    t = np.arange(15, 7000, 10)

    sp = plt.subplot(311)
    plt.ylabel(u'Jahresbeträge')
    net = map(netPerYear, t)
    si = map(siPerYear, t)
    it = map(itPerYear, t)
    plt.plot(t, net, label='Nettoeinkommen', linewidth=2.0)
    plt.plot(t, si, label='Sozialversicherung', linewidth=2.0, color="lightgreen")
    plt.plot(t, it, label='Lohnsteuer', linewidth=2.0, color="green")
    plt.legend(loc=2, prop={'size': 11})
    plt.grid(True)
    plt.xlabel("Brutto-Monatsgehalt")

    sp = plt.subplot(312)
    plt.ylabel(u'Abl. der Jahresbeträge')
    net = map(diffQuotient(netPerYear), t)
    si = map(diffQuotient(siPerYear), t)
    it = map(diffQuotient(itPerYear), t)
    plt.plot(t, net, label='Nettoeinkommen', linewidth=2.0)
    plt.plot(t, si, label='Sozialversicherung', linewidth=2.0, color="lightgreen")
    plt.plot(t, it, label='Lohnsteuer', linewidth=2.0, color="green")
    sp.set_ylim(0, 15)
    plt.legend(loc=1, prop={'size': 11})
    plt.grid(True)
    plt.xlabel("Brutto-Monatsgehalt")

    sp = plt.subplot(313)
    plt.ylabel(u'Relative Jahresbeträge')
    net = map(lambda x: netPerYear(x)/x/14, t)
    si = map(lambda x: siPerYear(x)/x/14, t)
    it = map(lambda x: itPerYear(x)/x/14, t)
    plt.plot(t, net, label='Nettoeinkommen', linewidth=2.0)
    plt.plot(t, si, label='Sozialversicherung', linewidth=2.0, color="lightgreen")
    plt.plot(t, it, label='Lohnsteuer', linewidth=2.0, color="green")
    sp.set_ylim(0, 1.1)
    plt.legend(loc=1, prop={'size': 11})
    plt.grid(True)
    plt.xlabel("Brutto-Monatsgehalt")


    plt.figure(2, figsize=(6.5, 8), dpi=80, facecolor='w')
    plt.subplots_adjust(left=0.13, right=0.95, bottom=0.06, top=0.98)

    sp = plt.subplot(311)
    plt.ylabel(u'Monatsbeträge')
    net = map(lambda x: netPerMonth(1, x), t)
    si = map(lambda x: siPerMonth(1, x), t)
    it = map(lambda x: itPerMonth(1, x), t)
    plt.plot(t, net, label='Nettoeinkommen', linewidth=2.0)
    plt.plot(t, si, label='Sozialversicherung', linewidth=2.0, color="lightgreen")
    plt.plot(t, it, label='Lohnsteuer', linewidth=2.0, color="green")
    plt.legend(loc=2, prop={'size': 11})
    plt.grid(True)
    plt.xlabel("Brutto-Monatsgehalt")

    sp = plt.subplot(312)
    plt.ylabel(u'Abl. der Monatsbeträge')
    net = map(diffQuotient(lambda x: netPerMonth(1,x)), t)
    si = map(diffQuotient(lambda x: siPerMonth(1,x)), t)
    it = map(diffQuotient(lambda x: itPerMonth(1,x)), t)
    plt.plot(t, net, label='Nettoeinkommen', linewidth=2.0)
    plt.plot(t, si, label='Sozialversicherung', linewidth=2.0, color="lightgreen")
    plt.plot(t, it, label='Lohnsteuer', linewidth=2.0, color="green")
    sp.set_ylim(0, 1.1)
    sp.grid(True)
    plt.legend(loc=1, prop={'size': 11})
    plt.xlabel("Brutto-Monatsgehalt")

    sp = plt.subplot(313)
    plt.ylabel(u'Relative Monatsbeträge')
    net = map(lambda x: netPerMonth(1, x)/x, t)
    si = map(lambda x: siPerMonth(1, x)/x, t)
    it = map(lambda x: itPerMonth(1, x)/x, t)
    plt.plot(t, net, label='Nettoeinkommen', linewidth=2.0)
    plt.plot(t, si, label='Sozialversicherung', linewidth=2.0, color="lightgreen")
    plt.plot(t, it, label='Lohnsteuer', linewidth=2.0, color="green")
    sp.set_ylim(0, 1.1)
    plt.legend(loc=1, prop={'size': 11})
    plt.grid(True)
    plt.xlabel("Brutto-Monatsgehalt")


    plt.figure(3, figsize=(6.5, 3), dpi=80, facecolor='w')
    plt.subplots_adjust(left=0.15, right=0.9, bottom=0.15, top=0.95)

    sp = plt.subplot(111)
    plt.ylabel(u'Nettogehälter')
    t = np.arange(1000, 2000, 10)
    net = map(lambda x: netPerMonth(1, x), t)
    net13 = map(lambda x: netPerMonth(13, x), t)
    net14 = map(lambda x: netPerMonth(14, x), t)
    plt.plot(t, net, label='1.-12. Monat', linewidth=2.0)
    plt.plot(t, net13, label='13. Monat', linewidth=2.0, color="lightgreen")
    plt.plot(t, net14, label='14. Monat', linewidth=2.0, color="green")
    plt.legend(loc=2, prop={'size': 11})
    plt.grid(True)
    plt.xlabel("Brutto-Monatsgehalt")

    plt.show()

def printUsage():
    print("""Usage:
  {0} -t gross-per-month
  {0} -p
  {0} -h""".format(sys.argv[0]))


if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hpt:")

        for opt, arg in opts:
            if opt == "-h":
                printUsage()
                sys.exit(os.EX_OK)
            if opt == "-p":
                showPlots()
            if opt == "-t":
                printTaxesTable(int(arg))

    except getopt.GetoptError as e:
        print("Error parsing arguments:", e)
        printUsage()

