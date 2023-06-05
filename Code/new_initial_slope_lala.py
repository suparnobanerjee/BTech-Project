# import pandas as pd
# import matplotlib.pyplot as plt
# import scipy.signal as sg
# import Function1 as fun
# import Function2 as fun2
# import xlsxwriter as xl
# from scipy.interpolate import CubicSpline
# import numpy as np


# def slope(lst):
#     slopes = []
#     peak_indices = sg.argrelmax(np.array(lst))[0]
#     if len(peak_indices) > 0:
#         i = peak_indices[0]
#         peak = lst[i]
#         j = i - 1
#         while lst[j] >= peak and j > 0:
#             j -= 1
#         if j > 0:
#             x1 = j
#             x2 = i
#             y1 = lst[j]
#             y2 = peak
#             slope = (y2 - y1) / (x2 - x1)
#             slopes.append(slope)
#     return slopes


# def count_Peak_Extremas(lst):
#     lst = np.array(lst)
#     maxpeak_indices = sg.argrelextrema(lst, np.greater)[0]
#     minpeak_indices = sg.argrelextrema(lst, np.less)[0]
#     return lst[maxpeak_indices], maxpeak_indices, lst[minpeak_indices], minpeak_indices


# Bigdata = []

# Name = ["Anish", "Avijit", "Aneshwa", "Sayan", "Sunny", "Shreya",
#         "Sudipta", "Sneha", "Koushik", "Moudud", "Srijita", "Pallabi"]

# wb = xl.Workbook('D:\DD\Slopes.xlsx')

# for k1 in range(len(Name)):
#     print(k1)
#     d = pd.read_excel("D:\DD\File_PPG_EDA.xlsx",
#                       sheet_name=Name[k1], header=None)
#     df = pd.DataFrame(d)

#     bnormPPG = list(df.loc[0:480000, 0])
#     bnormEDA = list(df.loc[0:480000, 2])

#     normPPG = fun.norm(fun.FilterP(fun.movmean(bnormPPG, 50)))
#     normEDA = fun.norm(fun.FilterE(fun.movmean(bnormEDA, 50)))

#     PPGdata = [normPPG[0:90000], normPPG[90000:180000], normPPG[180000:240000],
#                normPPG[240000:330000], normPPG[330000:390000], normPPG[390000:480000]]
#     EDAdata = [normEDA[0:90000], normEDA[90000:180000], normEDA[180000:240000],
#                normEDA[240000:330000], normEDA[330000:390000], normEDA[390000:480000]]

#     fil = []
#     fil1 = []
#     for i in range(6):

#         Maxpeak, Maxpos, Minpeak, Minpos = count_Peak_Extremas(PPGdata[i])
#         ft = [Maxpeak, Maxpos, Minpeak, Minpos]
#         fil.append(ft)

#         maxpeak, maxpos, minpeak, minpos = count_Peak_Extremas(
#             EDAdata[i])
#         ft1 = [maxpeak, maxpos, minpeak, minpos]
#         fil1.append(ft1)

#     Maxpeak1 = []
#     Maxpos1 = []
#     Minpeak1 = []
#     Minpos1 = []
#     maxpeak1 = []
#     maxpos1 = []
#     minpeak1 = []
#     minpos1 = []

#     for i in range(6):
#         Maxpeak1.append(fil[i][0])
#         Maxpos1.append(fil[i][1])
#         Minpeak1.append(fil[i][2])
#         Minpos1.append(fil[i][3])
#         maxpeak1.append(fil1[i][0])
#         maxpos1.append(fil1[i][1])
#         minpeak1.append(fil1[i][2])
#         minpos1.append(fil1[i][3])

#     Condition = ['Resting before Reading', 'Reading', 'Resting before Listening Music',
#                  'Listening Music', 'Resting before Arithmetic Calculation Task', 'Arithmetic Calculation Task']

#     ws = wb.add_worksheet(Name[k1])

#     for i in range(6):
#         ws.write(0, 0, 'Condition')
#         ws.write(0, 1, 'Slope EDA (^10^-5)')
#         ws.write(i+1, 0, Condition[i])
#         ws.write(i+1, 1, (np.mean(slope(EDAdata[i])))/(1E-5))
# wb.close()


import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import Function1 as fun
import Function2 as fun2
import xlsxwriter as xl


Bigdata = []

Name = ["Anish", "Avijit", "Aneshwa", "Sayan", "Sunny", "Shreya",
        "Sudipta", "Sneha", "Koushik", "Moudud", "Srijita", "Pallabi"]

wb = xl.Workbook('D:\DD\Features.xlsx')

for k1 in range(1, 2):
    print(k1)
    d = pd.read_excel("D:\DD\File_PPG_EDA.xlsx",
                      sheet_name=Name[k1], header=None)
    df = pd.DataFrame(d)

    # Load Raw Data:
    bnormEDA = list(df.loc[0:480000, 2])

    # Normalization:
    normEDA = fun.norm(fun.FilterE(fun.movmean(bnormEDA, 50)))

    EDAdata = [normEDA[0:90000], normEDA[90000:180000], normEDA[180000:240000],
               normEDA[240000:330000], normEDA[330000:390000], normEDA[390000:480000]]

    # fil = []
    fil1 = []

    for i in range(6):
        maxcount, maxpeak, maxpos, mincount, minpeak, minpos = fun.count_Peak_Minima_EDA(
            EDAdata[i])
        Maxl = len(maxpos)
        Minl = len(minpos)
        maxpeak11 = []
        maxpos11 = []
        value = 0.05
        if maxpos[0] > minpos[0]:
            if Maxl < Minl:
                kl = Maxl
            else:
                kl = Minl-1
            for i in range(kl):
                left_l = abs(maxpeak[i] - minpeak[i])
                right_l = abs(maxpeak[i] - minpeak[i+1])
                if left_l > value and right_l > value:
                    maxpos11.append(maxpos[i])
                    maxpeak11.append(maxpeak[i])
        else:
            for i in range(1, Minl):
                left_l = abs(maxpeak[i] - minpeak[i-1])
                right_l = abs(maxpeak[i] - minpeak[i])
                if left_l > value and right_l > value:
                    maxpos11.append(maxpos[i])
                    maxpeak11.append(maxpeak[i])

        ft1 = [maxcount, maxpeak11, maxpos11, mincount, minpeak, minpos]
        fil1.append(ft1)

    maxpeak1 = []
    maxpos1 = []
    minpeak1 = []
    minpos1 = []

    for i in range(6):
        maxpeak1.append(fil1[i][1])
        maxpos1.append(fil1[i][2])
        minpeak1.append(fil1[i][4])
        minpos1.append(fil1[i][5])

    Condition = ['Resting before Reading', 'Reading', 'Resting before Listening Music',
                 'Listening Music', 'Resting before Arithmetic Calculation Task', 'Arithmetic Calculation Task']

for i in range(6):
    plt.figure()
    plt.plot(EDAdata[i], 'g')
    plt.title('EDA '+Condition[i])
    plt.xlim([0, len(EDAdata[i])])
    plt.plot(maxpos1[i], maxpeak1[i], 'ro')
    # plt.plot(minpos1[i],minpeak1[i],'bo')
plt.show()
