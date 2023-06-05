import numpy as np
import scipy.signal as sg
from scipy.fft import fft , fftfreq
import math
import sympy as sym
import random
import statistics as stat


def Mean(D):
    x = 0
    for j in range(len(D)):
        x += D[j]
    return x/len(D)

#Sum:
def Sum(lst):
  s = 0
  for i in lst:
    s +=i
  return s

#Movingmean:
def movmean(a,n):
  a1 = []
  l = len(a)
  for i in range(l-(n-1)):
    a1.append(Sum(a[i:(i+n)])/n)
  for i in range(l-(n-1),l):
    a1.append(a[i])
  return a1

#Absolute Value:
def Abs(x):
    if x >= 0:
        return x
    else:
        return (-1)*x

def Round(lst,x):
  lst1 = [round(i,x) for i in lst]
  return lst1

# Findpeaks:
def findpeaks(a,b,x):
    i=1
    while i<len(a):
        if(a[i] - a[i-1] < x):
            a.remove(a[i])
            b.remove(b[i])
        else:
            i+=1
    return a,b

#Derivative:
def Derivative(x):
  d = [0]*len(x)
  # t = [i for i in range(len(x))]
  for i in range(len(x)-1):
    d[i] = (x[i+1]-x[i])
  d[-1] = (x[-1]-x[-2])
  return d

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

#Find peak and minima and count them:
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
    Diapos = []
    Diapeak = []
    M = Mean(lst)
    for i in range(1,len(lst)-1):
      if lst[i-1]<lst[i] and lst[i]>lst[i+1] and lst[i] > M:
        Maxpeak1.append(lst[i])
        Maxpos1.append(i)

      elif lst[i-1]>lst[i] and lst[i]<lst[i+1] and lst[i] < M:
        Minpeak1.append(lst[i])
        Minpos1.append(i)
    
    Maxpos , Maxpeak = findpeaks(Maxpos1,Maxpeak1,220)
    Maxcount = len(Maxpeak)
    
    Minpos , Minpeak = findpeaks(Minpos1,Minpeak1,220)
    Mincount = len(Minpeak)

    for i in range(len(Maxpos) - 1):
        gap = Maxpos[i] + 100
        Diapeak.append(lst[gap])
        Diapos.append(gap)

    return Maxcount,Maxpeak,Maxpos,Minpeak,Minpos,Diapeak,Diapos

def PeakInterval(lst):
  # input maxpos i.e Systolic Peak position
  lst1 = []
  for i in range(len(lst)-1):
    lst1.append(lst[i+1] - lst[i])
  return lst1

def HeartRate(lst):
  #input maxpos i.e Systolic Peak Position
  f = 500
  lst1 = [60*f/i for i in lst]
  return lst1

def T1T2T3h1h2(lst,lst1,lst2,lst6,lst7,lst8):
#input maxpos,minpos,diastolic_position,maxpeak,minpeak,diastolic_peak
  lst3 = []
  lst4 = []
  lst5 = []
  lst9 = []
  lst10 = []
  k = len(lst)
  l = len(lst1)
  m = len(lst2)
  

  if lst[0] > lst1[0]:

    if k<=l:
      a = k
    else:
      a = l

    for i in range(a):
      # T1:
      lst3.append(Abs(lst[i]-lst1[i]))
      # h1:
      lst9.append(Abs(lst6[i]-lst7[i]))

  elif lst[0] < lst1[0]:

    if k-1 <= l:
      a = k - 1
    else:
      a = l
    for i in range(a):
      # T1:
      lst3.append(Abs(lst[i+1]-lst1[i]))
      # h1:
      lst9.append(Abs(lst6[i+1]-lst7[i]))
  

  if lst[0] > lst1[0]:
    if k<l:
      b = k
    else:
      b = l-1
    for i in range(b):
      # T2:
      lst4.append(Abs(lst1[i+1]-lst[i]))

  elif lst[0] < lst1[0]:

    if k <= l:
      b = k
    else:
      b = l
    for i in range(b):
      # T2:
      lst4.append(Abs(lst1[i]-lst[i]))

  
  if lst2[0] > lst1[0]:
    if m<l:
      c = m
    else:
      c = l-1
    for i in range(c):
        # T3:
        lst5.append(Abs(lst1[i+1] - lst2[i]))
        # h2:
        lst10.append(Abs(lst8[i] - lst7[i+1]))
 
  elif lst2[0] < lst1[0]:

    if m <= l:
      c = m
    else:
      c = l
    for i in range(c):
        # T3:
        lst5.append(Abs(lst1[i] - lst2[i]))
        # h2:
        lst10.append(Abs(lst8[i] - lst7[i]))

  return lst3 , lst4 , lst5 , lst9 , lst10 

def featurelist(D):
    lst = []
    lst2 = []
    lst3 = []
    lst4 = []
    lst5 = []
    lst6 = []
    lst7 = []
    lst8 = []
    k = 2500
    for i in range(0,len(D),k):
        lst1 = D[i:i+k]
        Maxcount,Maxpeak,Maxpos,Minpeak,Minpos,Diapeak,Diapos = count_Peak_Minima_PPG(lst1)
        T11 , T21 , T31 , h11 , h21 = T1T2T3h1h2(Maxpos,Minpos,Diapos,Maxpeak,Minpeak,Diapeak)

        lst.append(Maxcount)
        a = PeakInterval(Maxpos)
        lst2.append(Mean(a))
        lst3.append(Mean(HeartRate(a)))
        lst4.append(Mean(T11))
        lst5.append(Mean(T21))
        lst6.append(Mean(T31))
        lst7.append(Mean(h11))
        lst8.append(Mean(h21))

    bf = Round(lst,3)
    cf = Round(lst2,3)
    df = Round(lst3,0)
    ef = Round(lst4,3)
    ff = Round(lst5,3)
    gf = Round(lst6,3)
    hf = Round(lst7,3)
    bcf = Round(lst8,3)
    
    return bf,cf,df,ef,ff,gf,hf,bcf

#Find peak and minima and count them:
def count_Peak_Minima_EDA(lst):

    maxcount = 0
    mincount = 0
    maxpeak = []
    maxpos = []
    minpeak = []
    minpos = []
    for i in range(1,len(lst)-1):
      k = 0
      if lst[i-1] - lst[i] < k and lst[i] - lst[i+1] > k:
        maxpeak.append(lst[i])
        maxpos.append(i)
        maxcount += 1

      elif lst[i-1] - lst[i] > k and lst[i] - lst[i+1] < k:
        minpeak.append(lst[i])
        minpos.append(i)
        mincount += 1

    # return maxcount,maxpeak,maxpos,mincount,minpeak,minpos
    return len(maxpos)

def count_Peak_Minima_EDAlist(D):

  lst1 = []
  lst2 = []
  k = 5000
  for i in range(0,len(D),k):
    lst1 = D[i:i+k]
    lst2.append(count_Peak_Minima_EDA(lst1))

  return lst2

def slope(lst):
    lst1 = []
    lst3 = []
    m = []
    k = 2500
    for i in range(0,len(lst),k):
        lst1 = (lst[i:i+k])
        for i in range(len(lst1)-1):
            lst3.append(Abs(lst1[i]-lst1[i+1]))
        m.append(Mean(lst3)*(10**6))
    return Round(m,3)
