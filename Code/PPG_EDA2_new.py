import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import Function1 as fun
import Function2 as fun2
import xlsxwriter as xl
import numpy as np
from scipy.interpolate import CubicSpline as CS


Bigdata = []

# All data except Koushik sir for problem in interpolation
Name = ["Anish", "Avijit", "Aneshwa", "Sayan", "Sunny", "Shreya",
        "Sudipta", "Sneha", "Moudud", "Srijita", "Pallabi"]

wb = xl.Workbook('F:\BT-2023_Project\Data\Interpolation1.xlsx')

for k1 in range(len(Name)):
    print(k1)
    d = pd.read_excel("F:\BT-2023_Project\Data\File_PPG_EDA.xlsx",
                      sheet_name=Name[k1], header=None)
    df = pd.DataFrame(d)
    worksheet = wb.add_worksheet(Name[k1])

    # Load Raw Data:
    bnormPPG = list(df.loc[0:480000, 0])
    bnormEDA = list(df.loc[0:480000, 2])

    # Normalization:
    normPPG = fun.norm(fun.FilterP(fun.movmean(bnormPPG, 50)))
    normEDA = fun.norm(fun.FilterE(fun.movmean(bnormEDA, 50)))

    PPGdata = [normPPG[0:90000], normPPG[90000:180000], normPPG[180000:240000],normPPG[240000:330000], normPPG[330000:390000], normPPG[390000:480000]]
    EDAdata = [normEDA[0:90000], normEDA[90000:180000], normEDA[180000:240000],normEDA[240000:330000], normEDA[330000:390000], normEDA[390000:480000]]

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

# Ulala
    for i in range(len(Condition)):
        worksheet.write(0, i, Condition[i])
    # Process the data for each condition
    start_time = 30000
    end_time = 60000
    sum_diff = []
    interp_values = []
    sum_diff_dict = {}

    for i in range(6):
        x = np.arange(len(EDAdata[i]))
        cs = CS(x[minpos1[i]], minpeak1[i], bc_type='natural')
        interp_vals = cs(x)
        interp_values.append(interp_vals)
        diff_vals = interp_vals[start_time:end_time] - EDAdata[i][start_time:end_time]
        diff_sum = sum([(abs(diff)**2) for diff in diff_vals])
        sum_diff.append(diff_sum)
        # plt.figure()
        # plt.subplot(211)
        # plt.plot(PPGdata[i])
        # plt.title('PPG '+Condition[i])
        # plt.xlim([0, len(PPGdata[i])])
        # plt.plot(Maxpos1[i], Maxpeak1[i], 'ro')
        # plt.plot(Minpos1[i], Minpeak1[i], 'bo')
        # plt.plot(Diapos1[i], Diapeak1[i], 'mo')
        # plt.subplot(212)
        # plt.plot(EDAdata[i], 'g')
        # plt.title('EDA '+Condition[i])
        # plt.xlim([0, len(EDAdata[i])])
        # plt.plot(maxpos1[i], maxpeak1[i], 'ro')
        # plt.plot(minpos1[i], minpeak1[i], 'bo')
        # plt.plot(interp_values[i], label='Cubic Spline')
        # plt.plot(EDAdata[i], 'g')
        # plt.plot(interp_vals, label='Cubic Spline')
        # plt.axvline(x=start_time, color='r', linestyle='--')
        # plt.axvline(x=end_time, color='r', linestyle='--')
        # plt.title(f'Condition: {Condition[i]}')
        # print(f'Sum of differences for {Condition[i]}: {sum_diff[i]}')
        sum_diff_dict[Condition[i]] = sum_diff[i]
        worksheet.write(1, i, sum_diff[i])
        sum_diff_dict[Condition[i]] = sum_diff[i]

        peaks = fun2.count_Peak_Minima_EDA(EDAdata[i][start_time:end_time])
        worksheet.write(3,i,peaks) # Peaks per 10 seconds

wb.close()
# plt.show()
