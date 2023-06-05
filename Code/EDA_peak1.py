import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import Function1 as fun
import Function2 as fun2
import xlsxwriter as xl
import numpy as np
from scipy.interpolate import CubicSpline


Bigdata = []

Name = ["Anish", "Avijit", "Aneshwa", "Sayan", "Sunny", "Shreya",
        "Sudipta", "Sneha", "Koushik", "Moudud", "Srijita", "Pallabi"]

wb = xl.Workbook('D:\DD\Data.xlsx')

for k1 in range(1):
    print(k1)
    d = pd.read_excel("D:\DD\File_PPG_EDA.xlsx",
                      sheet_name=Name[k1], header=None)
    df = pd.DataFrame(d)

    # Load Raw Data:
    bnormPPG = list(df.loc[0:480000, 0])
    bnormEDA = list(df.loc[0:480000, 2])

    # Normalization:
    normPPG = fun.norm(fun.FilterP(fun.movmean(bnormPPG, 50)))
    normEDA = fun.norm(fun.FilterE(fun.movmean(bnormEDA, 50)))

    PPGdata = [normPPG[0:90000], normPPG[90000:180000], normPPG[180000:240000],
               normPPG[240000:330000], normPPG[330000:390000], normPPG[390000:480000]]
    EDAdata = [normEDA[0:90000], normEDA[90000:180000], normEDA[180000:240000],
               normEDA[240000:330000], normEDA[330000:390000], normEDA[390000:480000]]

    fil = []
    fil1 = []
    for i in range(6):
        Maxcount, Maxpeak, Maxpos, Minpeak, Minpos, Diapeak, Diapos = fun2.count_Peak_Minima_PPG(
            PPGdata[i])
        ft = [Maxcount, Maxpeak, Maxpos, Minpeak, Minpos, Diapeak, Diapos]
        fil.append(ft)

        maxcount, maxpeak, maxpos, mincount, minpeak, minpos = fun.count_Peak_Minima_EDA(
            EDAdata[i])
        ft1 = [maxcount, maxpeak, maxpos, mincount, minpeak, minpos]
        fil1.append(ft1)

    Maxpeak1 = []
    Maxpos1 = []
    Minpeak1 = []
    Minpos1 = []
    Diapeak1 = []
    Diapos1 = []
    maxpeak1 = []
    maxpos1 = []
    minpeak1 = []
    minpos1 = []

    for i in range(6):
        Maxpeak1.append(fil[i][1])
        Maxpos1.append(fil[i][2])
        Minpeak1.append(fil[i][3])
        Minpos1.append(fil[i][4])
        Diapeak1.append(fil[i][5])
        Diapos1.append(fil[i][6])
        maxpeak1.append(fil1[i][1])
        maxpos1.append(fil1[i][2])
        minpeak1.append(fil1[i][4])
        minpos1.append(fil1[i][5])

    Condition = ['Resting before Reading', 'Reading', 'Resting before Listening Music',
                 'Listening Music', 'Resting before Arithmetic Calculation Task', 'Arithmetic Calculation Task']

# interpolation
interp_values = []
for i in range(len(minpos1)):
    x = np.arange(len(EDAdata[i]))
    cs = CubicSpline(x[minpos1[i]], minpeak1[i], bc_type='natural')
    interp_vals = cs(x)
    interp_values.append(interp_vals)


# for i in range(6):
#     plt.figure()
#     plt.subplot(211)
#     plt.plot(PPGdata[i])
#     plt.title('PPG '+Condition[i])
#     plt.xlim([0, len(PPGdata[i])])
#     plt.plot(Maxpos1[i], Maxpeak1[i], 'ro')
#     plt.plot(Minpos1[i], Minpeak1[i], 'bo')
#     plt.plot(Diapos1[i], Diapeak1[i], 'mo')
#     plt.subplot(212)
#     plt.plot(EDAdata[i], 'g')
#     plt.title('EDA '+Condition[i])
#     plt.xlim([0, len(EDAdata[i])])
#     plt.plot(maxpos1[i], maxpeak1[i], 'ro')
#     plt.plot(minpos1[i], minpeak1[i], 'bo')
#     plt.plot(interp_values[i], label='Cubic Spline')
# plt.show()

for i in range(6):
    plt.figure()
    plt.plot(EDAdata[i], 'g', label='EDA')
    plt.plot(maxpos1[i], maxpeak1[i], 'ro', label='Phasic Peaks')
    plt.plot(minpos1[i], minpeak1[i], 'bo', label='Tonic Peaks')
    plt.plot(interp_values[i], label='Cubic Spline')
    plt.title('EDA ' + Condition[i])
    plt.xlim([0, len(EDAdata[i])])
    plt.legend()
    plt.show()
