import numpy as np
import scipy.signal as sg
from scipy.fft import fft, fftfreq
import math
import sympy as sym
import random
import matplotlib.pyplot as plt


D = []
D1 = []
for i in range(10):
    D.append(random.randint(0, 50))
    D1.append(random.randint(0, 100))
x = D
t = D1

# Absolute Value:


def Abs(x):
    if x >= 0:
        return x
    else:
        return (-1)*x


def Round(lst, x):
    lst1 = [round(i, x) for i in lst]
    return lst1

# Bubble Sort:


def Sort(lst):
    a = len(lst)
    for i in range(a-1):
        for j in range(a-i-1):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst

# Maximum Value:


def Max(lst):
    Sort(lst)
    return lst[-1]

# Minimum Value:


def Min(lst):
    Sort(lst)
    return lst[0]

# Square Root:


def Sqrt(n):
    return n**0.5


# Sum:
def Sum(lst):
    s = 0
    for i in lst:
        s += i
    return s

# Mean:


def Mean(D):
    x = 0
    for i in range(len(D)):
        x += D[i]
    return x/(i+1)

# Meanlist:


def Meanlist(D):
    lst1 = []
    lst2 = []
    k = 2500
    for i in range(0, len(D), k):
        lst1 = D[i:i+k]
        lst2.append(Mean(lst1))
    return Round(lst2, 4)


# Standard Deviation:
def sd(D):
    x = 0
    y = Mean(D)
    for i in range(len(D)):
        x += (D[i] - y)**2
    return Sqrt(x/i)


def sdlist(D):
    lst1 = []
    lst2 = []
    k = 2500
    for i in range(0, len(D), k):
        lst1 = D[i:i+k]
        lst2.append(sd(lst1))
    return Round(lst2, 5)


# Variance:
def var(D):
    return sd(D)**2


def varlist(D):
    lst1 = []
    lst2 = []
    k = 2500
    for i in range(0, len(D), k):
        lst1 = D[i:i+k]
        lst2.append(var(lst1)*(10**6))
    return Round(lst2, 2)

# Derivative:


def Derivative(x):
    d = [0]*len(x)
    # t = [i for i in range(len(x))]
    for i in range(len(x)-1):
        d[i] = (x[i+1]-x[i])
    d[-1] = (x[-1]-x[-2])
    return d


# Movingmean:
def movmean(a, n):
    a1 = []
    l = len(a)
    for i in range(l-(n-1)):
        a1.append(Sum(a[i:(i+n)])/n)
    for i in range(l-(n-1), l):
        a1.append(a[i])
    return a1


# Normalization:
def norm(D):
    a = max(D)
    b = min(D)
    D = [Abs((i - b)/(a - b)) for i in D]
    return D

# Filter:


def FilterP(D):
    rp = 15  # Passband Ripple
    rs = 50  # Stopband Ripple
    Fs = 500  # Sampling frequency
    fn = Fs/2  # Nquist frequency
    fp = [0.3, 1]
    fs = [0.1, 30]
    wp = [i/fn for i in fp]
    ws = [i/fn for i in fs]
    n, wn = sg.buttord(wp, ws, rp, rs)
    b, a = sg.butter(n, wn, 'band', analog=True)
    return sg.filtfilt(b, a, D)


def FilterE(D):
    rp = 3  # Passband Ripple
    rs = 15  # Stopband Ripple
    Fs = 500  # Sampling frequency
    fn = Fs/2  # Nquist frequency
    fp = [0.0003, 0.3]
    fs = [0.0001, 0.8]
    wp = [i/fn for i in fp]
    ws = [i/fn for i in fs]
    n, wn = sg.buttord(wp, ws, rp, rs)
    b, a = sg.butter(n, wn, 'band')
    return sg.filtfilt(b, a, D)

# PPG features(P/L ratios):


def leftlimb(lst1, lst2, lst3, lst4):

    lst6 = []
    for i in range(len(lst2)-1):
        lst5 = (lst1[lst2[i]:lst3[i]])
        lst5 = np.asarray(lst5)
        lst6.append(lst2[i] + (np.abs(lst5 - lst4[i])).argmin())
    return lst6


def rightlimb(lst1, lst2, lst3, lst4):

    lst6 = []
    for i in range(len(lst3)-1):
        lst5 = (lst1[lst2[i]:lst3[i+1]])
        lst5 = np.asarray(lst5)
        lst6.append(lst2[i] + (np.abs(lst5 - lst4[i])).argmin())
    return lst6

# Total Power:


def powdb(lst):
    T = 500
    return math.log10(Sum(i**2/T for i in lst))


def powdblist(D):
    lst1 = []
    lst2 = []
    k = 2500
    for i in range(0, len(D), k):
        lst1 = D[i:i+k]
        lst2.append(powdb(lst1))
    return Round(lst2, 3)


def HeartRate(lst):
    # input maxpos i.e Systolic Peak Position
    f = 500
    lst1 = [60*f/i for i in lst]
    return lst1


def HeartRatelist(D):
    lst1 = []
    lst2 = []
    k = 2500
    for i in range(0, len(D), k):
        lst1 = D[i:i+k]
        lst2.append(HeartRate(Mean(lst1)))
    return lst2


def T1T2T3h1h2(lst, lst1, lst2, lst6, lst7, lst8):
    # input maxpos,minpos,diastolic_position,maxpeak,minpeak,diastolic_peak
    lst3 = []
    lst4 = []
    lst5 = []
    lst9 = []
    lst10 = []
    k = len(lst)
    l = len(lst1)
    m = len(lst2)

    if k <= l:
        a = k
    else:
        a = l
    for i in range(a):
        # T1:
        lst3.append(lst[i]-lst1[i])
        # h1:
        lst9.append(lst6[i]-lst7[i])

    if k < l:
        a = k
    else:
        a = l-1
    for i in range(a):
        # T3:
        lst4.append(lst1[i+1]-lst[i])

    if m < l:
        a = m
    else:
        a = l-1
    for i in range(a):
        # T2:
        lst5.append(lst1[i+1]-lst2[i])
        # h2:
        lst10.append(lst8[i]-lst7[i+1])
    return lst3, lst4, lst4, lst9, lst10


def T1T2T3h1h2list(D1, D2, D3, D4, D5):
    D = [D1, D2, D3, D4, D5]
    lst1 = []
    lst2 = []
    lst3 = []
    lst4 = []
    k = 2500
    for i in range(len(D)):
        for j in range(0, len(D[i]), k):
            d = D[i]
            lst1 = d[j:j+k]
            lst2.append(Mean(lst1))
            if d == D[0]:
                lst4.append(len(lst1))
        lst3.append(lst2)

    return lst3[0], lst3[1], lst3[2], lst3[3], lst3[4], lst4


def FFT(lst):

    Y = fft(lst)
    L = len(Y)
    # P2 = [Abs(i/L) for i in Y]
    P2 = [abs(i/L)**2 for i in Y]
    P1 = P2[:L//2]
    P1 = [2*i for i in P1]
    Fs = 500
    f = [Fs*i/L for i in range(L//2)]
    for i in range(len(P1)):
        if max(P1) == P1[i]:
            return f[i]


def FFTlist(D):
    lst1 = []
    lst2 = []
    k = 2500
    for i in range(0, len(D), k):
        lst1 = D[i:i+k]
        lst2.append(FFT(lst1))
    return lst2


# Find peak and minima and count them:


def count_Peak_Minima_PPG(lst):

    Maxcount = 0
    Mincount = 0
    Maxpeak = []
    Maxpos = []
    Maxpeak1 = []
    Maxpos1 = []
    Minpeak = []
    Minpos = []
    Minpeak1 = []
    Minpos1 = []
    M = Mean(lst)
    for i in range(1, len(lst)-1):
        if lst[i-1] < lst[i] and lst[i] > lst[i+1] and lst[i] > M:
            Maxpeak1.append(lst[i])
            Maxpos1.append(i)

        elif lst[i-1] > lst[i] and lst[i] < lst[i+1] and lst[i] < M:
            Minpeak1.append(lst[i])
            Minpos1.append(i)

    for i in range(len(Maxpos1)-1):
        if Maxpos1[i+1] - Maxpos1[i] > 200:
            Maxpos.append(Maxpos1[i])
            Maxpeak.append(Maxpeak1[i])
            Maxcount += 1
    Maxpos.append(Maxpos1[-1])
    Maxpeak.append(Maxpeak1[-1])
    Maxcount += 1

    for i in range(len(Minpos1)-1):
        if Minpos1[i+1] - Minpos1[i] > 200:
            Minpos.append(Minpos1[i])
            Minpeak.append(Minpeak1[i])
            Mincount += 1
    Minpos.append(Minpos1[-1])
    Minpeak.append(Minpeak1[-1])
    Mincount += 1

    return Maxcount, Maxpeak, Maxpos, Mincount, Minpeak, Minpos


def PeakInterval(lst):
    # input maxpos i.e Systolic Peak position
    lst1 = []
    for i in range(len(lst)-1):
        lst1.append(lst[i+1] - lst[i])
    return lst1

# Find peak and minima and count them:


def count_Peak_Minima_EDA(lst):

    maxcount = 0
    mincount = 0
    maxpeak = []
    maxpos = []
    minpeak = []
    minpos = []
    for i in range(1, len(lst)-1):
        k = 0
        if lst[i-1] - lst[i] < k and lst[i] - lst[i+1] > k:
            maxpeak.append(lst[i])
            maxpos.append(i)
            maxcount += 1

        elif lst[i-1] - lst[i] > k and lst[i] - lst[i+1] < k:
            minpeak.append(lst[i])
            minpos.append(i)
            mincount += 1

    return maxcount, maxpeak, maxpos, mincount, minpeak, minpos

    # Find peak and minima and count them:


def count_Peak_Minima_EDAlist(D):

    lst1 = []
    lst2 = []
    k = 2500
    for i in range(0, len(D), k):
        lst1 = D[i:i+k]
        lst2.append(len(count_Peak_Minima_EDA(lst1)))
    return lst2


def count_Peak_Minima_PPG_Diastolic(lst, lst1):
    # input 2nd Derivative , Filter data
    maxcount = 0
    mincount = 0
    maxpeak = []
    maxpos = []
    maxpeak1 = []
    maxpos1 = []
    minpeak = []
    minpos = []
    minpeak1 = []
    minpos1 = []
    Diapeak = []
    M = Mean(lst)
    for i in range(1, len(lst)-1):
        if lst[i-1] < lst[i] and lst[i] > lst[i+1] and lst[i] > M:
            maxpeak1.append(lst[i])
            maxpos1.append(i)

        elif lst[i-1] > lst[i] and lst[i] < lst[i+1] and lst[i] < M:
            minpeak1.append(lst[i])
            minpos1.append(i)

    for i in range(len(maxpos1)-1):
        if maxpos1[i+1] - maxpos1[i] > 100:
            maxpos.append(maxpos1[i])
            maxpeak.append(maxpeak1[i])
            maxcount += 1
    maxpos.append(maxpos1[-1])
    maxpeak.append(maxpeak1[-1])
    maxcount += 1

    for i in range(len(maxpos)-2):
        for j in range(len(minpos1)):
            k = minpos1[j] - maxpos[i]
            if k > 180 and k < 230:
                minpos.append(minpos1[j])
                minpeak.append(minpeak1[j])
                mincount += 1
                break

    Diapos = [i+30 for i in minpos]
    for i in Diapos:
        Diapeak.append(lst1[i])

    return maxcount, maxpeak, maxpos, mincount, minpeak, minpos, Diapeak, Diapos


# def slope(lst):
#     lst1 = []
#     lst3 = []
#     m = []
#     k = 2500
#     for i in range(0, len(lst), k):
#         lst1 = (lst[i:i+k])
#         for i in range(len(lst1)-1):
#             lst3.append(Abs(lst1[i]-lst1[i+1]))
#         m.append(Mean(lst3))
#     return Round(m, 8)


def slope(lst):
    slopes = []
    peak_indices = sg.argrelmax(np.array(lst))[0]
    for i in peak_indices:
        peak = lst[i]
        j = i - 1
        while lst[j] >= peak and j > 0:
            j -= 1
        segment = lst[j:i+1]
        slope = np.mean(np.gradient(segment))
        slopes.append(slope)
    return slopes
