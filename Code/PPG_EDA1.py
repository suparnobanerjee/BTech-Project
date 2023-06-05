import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import Function1 as fun
import Function2 as fun2
import xlsxwriter as xl

Bigdata = []

Name = ["Anish", "Avijit", "Aneshwa", "Sayan", "Sunny", "Shreya",
        "Sudipta", "Sneha", "Koushik", "Moudud", "Srijita", "Pallabi"]

wb = xl.Workbook('D:\DD\Data1.xlsx')

for k1 in range(0, 1):
    print(k1)
    d = pd.read_excel("D:\DD\File_PPG_EDA.xlsx",
                      sheet_name=Name[k1], header=None)
    df = pd.DataFrame(d)

    # Load Raw Data:
    bnormPPG = list(df.loc[0:479999, 0])
    bnormEDA = list(df.loc[0:479999, 2])

    # Normalization:
    normPPG = fun.norm(fun.FilterP(fun.movmean(bnormPPG, 50)))
    normEDA = fun.norm(fun.FilterE(fun.movmean(bnormEDA, 50)))

    PPGdata = [normPPG[10000:40000], normPPG[110000:140000], normPPG[210000:240000],
               normPPG[265000:295000], normPPG[330000:360000], normPPG[390000:420000]]
    EDAdata = [normEDA[10000:40000], normEDA[110000:140000], normEDA[210000:240000],
               normEDA[265000:295000], normEDA[330000:360000], normEDA[390000:420000]]

    Average = []
    Standard_Deviation = []
    Variance = []
    Power = []
    Fast_Fourier_Transform = []
    Number_of_Peaks = []
    Peak_Interval = []
    Heart_Rate = []
    T1 = []
    T2 = []
    T3 = []
    h1 = []
    h2 = []
    Average12 = []
    Standard_Deviation12 = []
    Variance12 = []
    Power12 = []
    Slope = []
    Number_of_Peaks12 = []

    ft = []
    for i in PPGdata:
        bf, cf, df, ef, ff, gf, hf, bcf = fun2.featurelist(i)
        N1 = [bf, cf, df, ef, ff, gf, hf, bcf]
        ft.append(N1)

    # PPG:
    for i in PPGdata:
        Average.append(fun.Meanlist(i))
        Standard_Deviation.append(fun.sdlist(i))
        Variance.append(fun.varlist(i))
        Power.append(fun.powdblist(i))
        Fast_Fourier_Transform.append(fun.FFTlist(i))

    for i in range(len(ft)):
        Number_of_Peaks.append(ft[i][0])
        Peak_Interval.append(ft[i][1])
        Heart_Rate.append(ft[i][2])
        T1.append(ft[i][3])
        T2.append(ft[i][4])
        T3.append(ft[i][5])
        h1.append(ft[i][6])
        h2.append(ft[i][7])

    PD = [Average, Standard_Deviation, Variance, Power, Fast_Fourier_Transform,
          Number_of_Peaks, Peak_Interval, Heart_Rate, T1, T2, T3, h1, h2]
    PD1 = ["Average", "Standard_Deviation", "Variance[10^6]", "Power", "Fast_Fourier_Transform",
           "Number_of_Peaks", "Peak_Interval", "Heart_Rate", "T1", "T2", "T3", "h1", "h2"]

    Avav = []
    sdav = []
    varav = []
    powav = []
    fastav = []
    peaksav = []
    peakinav = []
    hrateav = []
    T1av = []
    T2av = []
    T3av = []
    h1av = []
    h2av = []

    for i in range(len(PD)):
        for j in PD[i]:
            if i == 0:
                Avav.append(fun.Mean(j))
            elif i == 1:
                sdav.append(fun.Mean(j))
            elif i == 2:
                varav.append(round(fun.Mean(j), 2))
            elif i == 3:
                powav.append(fun.Mean(j))
            elif i == 4:
                fastav.append(fun.Mean(j))
            elif i == 5:
                peaksav.append(round(fun.Mean(j), 0))
            elif i == 6:
                peakinav.append(fun.Mean(j))
            elif i == 7:
                hrateav.append(round(fun.Mean(j), 0))
            elif i == 8:
                T1av.append(fun.Mean(j))
            elif i == 9:
                T2av.append(fun.Mean(j))
            elif i == 10:
                T3av.append(fun.Mean(j))
            elif i == 11:
                h1av.append(fun.Mean(j))
            elif i == 12:
                h2av.append(fun.Mean(j))

    PDav = [Avav, sdav, varav, powav, fastav, peaksav,
            peakinav, hrateav, T1av, T2av, T3av, h1av, h2av]

    # EDA:
    for i in EDAdata:
        Average12.append(fun.Meanlist(i))
        Standard_Deviation12.append(fun.sdlist(i))
        Variance12.append(fun.varlist(i))
        Power12.append(fun.powdblist(i))
        Slope.append(fun2.slope(i))
        Number_of_Peaks12.append(fun2.count_Peak_Minima_EDAlist(i))

    ED = [Average12, Standard_Deviation12,
          Variance12, Power12, Slope, Number_of_Peaks12]
    ED1 = ["Average", "Standard_Deviation", "Variance[10^6]",
           "Power", "Slope[10^6]", "Number_of_Peaks"]

    Avav1 = []
    sdav1 = []
    varav1 = []
    powav1 = []
    slav = []
    peaks1av = []

    for i in range(len(ED)):
        for j in ED[i]:
            if i == 0:
                Avav1.append(fun.Mean(j))
            elif i == 1:
                sdav1.append(fun.Mean(j))
            elif i == 2:
                varav1.append(round(fun.Mean(j), 2))
            elif i == 3:
                powav1.append(fun.Mean(j))
            elif i == 4:
                slav.append(round(fun.Mean(j), 3))
            elif i == 5:
                peaks1av.append(round(fun.Mean(j), 0))

    EDav = [Avav1, sdav1, varav1, powav1, slav, peaks1av]

    ws = wb.add_worksheet(Name[k1])

    # f1 = wb.add_format({'bold': True , 'fontcolor' : 'brown' , 'fontsize' : 14 })
    # f2 = wb.add_format({'bold': True , 'fontcolor' : 'green' , 'fontsize' : 12 })

    column = 2
    row = 0
    for i in PD1:
        ws.write(row, column, i)
        column += 9

    column = 0
    for k in PD:
        for i in k:
            row = 1
            for j in i:
                ws.write(row, column, j)
                row += 1
            column += 1
        column += 3

    column = 2
    row = 19
    for i in ED1:
        ws.write(row, column, i)
        column += 9

    column = 0
    for k in ED:
        for i in k:
            row = 20
            for j in i:
                ws.write(row, column, j)
                row += 1
            column += 1
        column += 3

    row = 35
    for i in PDav:
        column = 1
        for j in i:
            ws.write(row, column, j)
            column += 1
        row += 1

    row = 35
    for i in EDav:
        column = 10
        for j in i:
            ws.write(row, column, j)
            column += 1
        row += 1

    row = 35
    column = 0
    for i in PD1:
        ws.write(row, column, i)
        row += 1

    row = 35
    column = 9
    for i in ED1:
        ws.write(row, column, i)
        row += 1

wb.close()
