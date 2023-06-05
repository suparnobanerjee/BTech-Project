import numpy as np
import scipy.signal as sg
import math
import scipy.fft as spf
import sympy as sym
import random


# D = []
# D1 = []
# for i in range(10):
#     D.append(random.randint(0,50))
#     D1.append (random.randint(0,100))
# x = D
# t = D1


#Absolute Value:
def Abs(x):
    if x >= 0:
        return x
    else:
        return (-1)*x

#Bubble Sort:
def Sort(lst):
    a = len(lst)
    for i in range(a-1):
        for j in range(a-i-1):
            if lst[j] > lst[j+1]:
                lst[j] , lst[j+1] = lst[j+1] , lst[j]
    return lst

#Maximum Value:
def Max(lst):
    Sort(lst)
    return lst[-1]

#Minimun Value:
def Min(lst):
    Sort(lst)
    return lst[0]


#Square Root:
def Sqrt(n):
  return n**0.5

#Sum:
def Sum(lst):
  s = 0
  for i in lst:
    s +=i
  return s

#Mean:
def Mean(D):
    x = 0
    for i in range(len(D)):
        x += D[i]
    return x/(i+1)

#Standard Deviation:
def sd(D):
    x = 0
    y = Mean(D)
    for i in range(len(D)):
        x += (D[i] - y)**2
    return Sqrt(x/i)

#Variance:
def var(D):
    return sd(D)**2

#Derivative:
def Derivative(x):
  d = [0]*len(x)
  # t = [i for i in range(len(x))]
  for i in range(len(x)-1):
    d[i] = (x[i+1]-x[i])
  d[-1] = (x[-1]-x[-2])
  return d


#Movingmean:
def movmean(a,n):
  a1 = []
  l = len(a)
  for i in range(l-(n-1)):
    a1.append(Sum(a[i:(i+n)])/n)
  for i in range(l-(n-1),l):
    a1.append(a[i])
  return a1


#Normalization:
def norm(D):
    a = max(D)
    b = min(D)
    D = [Abs((i - b)/(a - b)) for i in D]
    return D

#Filter:
def FilterP(D):
  rp = 15    #Passband Ripple
  rs = 50    #Stopband Ripple
  Fs = 500    #Sampling frequency
  fn = Fs/2   #Nquist frequency
  fp = [0.3,1]
  fs = [0.1,30]
  wp = [i/fn for i in fp]
  ws = [i/fn for i in fs]
  n,wn = sg.buttord(wp,ws,rp,rs)
  b,a = sg.butter(n,wn,'band', analog = True)
  return sg.filtfilt(b,a,D)

def FilterE(D):
  rp = 3    #Passband Ripple
  rs = 15    #Stopband Ripple
  Fs = 500    #Sampling frequency
  fn = Fs/2   #Nquist frequency
  fp = [0.0003,0.3]
  fs = [0.0001,0.8]
  wp = [i/fn for i in fp]
  ws = [i/fn for i in fs]
  n,wn = sg.buttord(wp,ws,rp,rs)
  b,a = sg.butter(n,wn,'band')
  return sg.filtfilt(b,a,D)

# PPG features(P/L ratios):
def leftlimb(lst1,lst2,lst3,lst4):

  lst6 = []
  for i in range(len(lst2)-1):
    lst5 = (lst1[lst2[i]:lst3[i]])
    lst5 = np.asarray(lst5)
    lst6.append(lst2[i] + (np.abs(lst5 - lst4[i])).argMin())  
  return lst6

def rightlimb(lst1,lst2,lst3,lst4):

  lst6 = []
  for i in range(len(lst3)-1):
    lst5 = (lst1[lst2[i]:lst3[i+1]])
    lst5 = np.asarray(lst5)
    lst6.append(lst2[i] + (np.abs(lst5 - lst4[i])).argMin())  
  return lst6

#Total Power:
def powdb(lst):
    T = 500
    return math.log10(Sum(i**2/T for i in lst)) 

def PeakInterval(lst):
  k = len(lst)-1
  lst1 = [0]*k
  for i in range(k):
    lst1[i] = lst1[i+1] - lst1[i]
  return lst1

def HeartRate(lst):
  f = 500
  lst1 = [60*f/i for i in lst]
  return lst1

def T1T2T3h1h2(lst,lst1,lst2,lst6,lst7,lst8):
#input Maxpos,Minpos,diastolic_position,Maxpeak,Minpeak,diastolic_peak
  lst3 = []
  lst4 = []
  lst5 = []
  lst9 = []
  lst10 = []
  k = len(lst)
  l = len(lst1)
  b = 0
  for i in range(k):
      lst3.append(lst[i]-lst1[i])
      lst9.append(lst6[i]-lst7[i])
  
  if k+1 == l:
    m = k
  elif k == l:
    m = k-1
  for i in range(m):
      lst4.append(lst1[i+1]-lst[i])
      lst5.append(lst1[i+1]-lst2[i])
      lst10.append(lst8[i]-lst7[i+1])
  return lst3 ,lst4 , lst4, lst9 ,lst10


def FFT(lst):

  N = len(lst)
  T = 1/500
  yf = abs(spf.fft(lst))
  xf = abs(spf.fftfreq(N,T))
  return xf,yf
       

#Find peak and Minima and count them:
def count_Peak_Minima_EDA(lst):

    Maxcount = 0
    Mincount = 0
    Maxpeak = []
    Maxpos = []
    Minpeak = []
    Minpos = []
    for i in range(1,len(lst)-1):
      if lst[i-1]<lst[i] and lst[i]>lst[i+1]:
        Maxpeak.append(lst[i])
        Maxpos.append(i)
        Maxcount += 1

      elif lst[i-1]>lst[i] and lst[i]<lst[i+1]:
        Minpeak.append(lst[i])
        Minpos.append(i)
        Mincount += 1

    return Maxcount,Maxpeak,Maxpos,Mincount,Minpeak,Minpos

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
    for i in range(1,len(lst)-1):
      if lst[i-1]<lst[i] and lst[i]>lst[i+1] and lst[i] > M:
        Maxpeak1.append(lst[i])
        Maxpos1.append(i)

      elif lst[i-1]>lst[i] and lst[i]<lst[i+1] and lst[i] < M:
        Minpeak1.append(lst[i])
        Minpos1.append(i)
    
    for i in range(len(Maxpos1)-1):
      if Maxpos1[i+1] - Maxpos1[i]>200:
        Maxpos.append(Maxpos1[i])     
        Maxpeak.append(Maxpeak1[i])
        Maxcount += 1
    Maxpos.append(Maxpos1[-1])
    Maxpeak.append(Maxpeak1[-1])
    Maxcount += 1

    for i in range(len(Minpos1)-1):
      if Minpos1[i+1] - Minpos1[i]>200:
        Minpos.append(Minpos1[i])
        Minpeak.append(Minpeak1[i])
        Mincount += 1
    Minpos.append(Minpos1[-1])
    Minpeak.append(Minpeak1[-1])
    Mincount += 1

    return Maxcount,Maxpeak,Maxpos,Mincount,Minpeak,Minpos

def count_Peak_Minima_PPG_Diastolic(lst,lst1):

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
    Diapeak = []
    M = Mean(lst)
    for i in range(1,len(lst)-1):
      if lst[i-1]<lst[i] and lst[i]>lst[i+1] and lst[i] > M:
        Maxpeak1.append(lst[i])
        Maxpos1.append(i)

      elif lst[i-1]>lst[i] and lst[i]<lst[i+1] and lst[i] < M:
        Minpeak1.append(lst[i])
        Minpos1.append(i)
    
    for i in range(len(Maxpos1)-1):
      if Maxpos1[i+1] - Maxpos1[i]>100:
        Maxpos.append(Maxpos1[i])     
        Maxpeak.append(Maxpeak1[i])
        Maxcount += 1
    Maxpos.append(Maxpos1[-1])
    Maxpeak.append(Maxpeak1[-1])
    Maxcount += 1

    for i in range(len(Maxpos)-2):
        for j in range(len(Minpos1)):
            k = Minpos1[j] - Maxpos[i]
            if k > 180 and k<230:
                Minpos.append(Minpos1[j])
                Minpeak.append(Minpeak1[j])
                Mincount +=1
                break

    Diapos = [i+ 30 for i in Minpos]
    for i in Diapos:
        Diapeak.append(lst1[i])

    return Maxcount,Maxpeak,Maxpos,Mincount,Minpeak,Minpos,Diapeak,Diapos

def slope(lst):
    lst1 = []
    lst2 = []
    lst3 = []
    m = []
    k = 2500
    for i in range(0,len(lst),k):
        lst1 = (lst[i:i+k])
        lst2 = [i for i in range(i+k)]
        for i in range(len(lst1)-1):
            lst3.append(Abs((lst1[i]-lst1[i+1])/(lst2[i]-lst2[i+1])))
        m.append(round(Mean(lst3),6))
    return m
  


