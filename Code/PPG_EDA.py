import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import Function as fun
import Function1 as fun1
import Function2 as fun2
import xlsxwriter as xl


d = pd.read_excel("D:\\DD\\File_PPG_EDA.xlsx",
                  sheet_name='Shreya', header=None)
df = pd.DataFrame(d)

x = int(input("Press '1' for Resting before Reading\nPress '2' for Reading\nPress '3' for Resting before Listening Music\nPress '4' for Listening Music\nPress '5' for Resting before Arithmetic Calculation Task\nPress '6' for Arithmetic Calculation Task\nPress '7' for Whole data\n"))


if x == 1:
    PPGdata = list(df.loc[60000:89999, 0])
    EDAdata = list(df.loc[0:89999, 2])
    m = "Resting before Reading"

elif x == 2:
    PPGdata = list(df.loc[90000:119999, 0])
    EDAdata = list(df.loc[90000:179999, 2])
    m = "Reading"
elif x == 3:
    PPGdata = list(df.loc[210000:239999, 0])
    EDAdata = list(df.loc[180000:239999, 2])
    m = "Resting before Listening Music"
elif x == 4:
    PPGdata = list(df.loc[240000:269999, 0])
    EDAdata = list(df.loc[240000:329999, 2])
    m = "Listening Music"
elif x == 5:
    PPGdata = list(df.loc[360000:389999, 0])
    EDAdata = list(df.loc[330000:389999, 2])
    m = "Resting before Arithmetic Calculation Task"
elif x == 6:
    PPGdata = list(df.loc[390000:419999, 0])
    EDAdata = list(df.loc[390000:479999, 2])
    m = "Arithmetic Calculation Task"
elif x == 7:
    PPGdata = list(df.loc[0:479999, 0])
    EDAdata = list(df.loc[0:479999, 2])
    m = "Whole data"
else:
    exit(0)


D1 = [i+20 for i in PPGdata]
D2 = [i+20 for i in EDAdata]


D1 = fun.norm(fun.FilterP(fun.movmean(D1, 20)))
D2 = fun.norm(fun.FilterE(D2))


dt = [D1, D2]


xf, yf = fun.FFT(D1)
plt.plot(xf, yf)
plt.show()

# Average = fun.Mean(D1)
# Stdev = fun.sd(D1)
# Variance = fun.var(D1)
# Power = fun.powdb(D1)
# maxcount,maxpeak,maxpos,minpeak,minpos,Diapeak,Diapos = fun2.count_Peak_Minima_PPG(D1)

# Average1 = fun.Mean(D2)
# Stdev1 = fun.sd(D2)
# Variance1 = fun.var(D2)
# Power1 = fun.powdb(D2)
# maxcount1,maxpeak1,maxpos1,mincount1,minpeak1,minpos1 = fun.count_Peak_Minima_EDA(D2)


# dt1 = ["Average" , "Standard Deviation" , "Variance" , "Power" , "Number of Peaks"]
# dt2 = [Average , Stdev , Variance , Power , maxcount]

# #Plot:
# for i in range(len(dt)):
#   plt.subplot(len(dt),1,i+1)
#   plt.plot(dt[i])
#   plt.xlim([0,len(dt[i])])
#   if i == 0:
#     plt.ylabel('Amplitude of Voltage ')
#   elif i == 1:
#     plt.ylabel('Amplitude of Conductance ')
#   plt.xlabel('Time in miliseconds')
#   plt.title(m)


# #Write in excel:
# workbook = xl.Workbook('D:\DD\Features.xlsx')
# worksheet = workbook.add_worksheet("Sheet1")

# row = 0
# column = 1

# for item in dt1:
#   worksheet.write(row,column,item)
#   column +=1
# row +=1
# column = 1
# for item in dt2:
#   worksheet.write(row,column,item)
#   column +=1
# worksheet.write(1,0,m)
# workbook.close()
