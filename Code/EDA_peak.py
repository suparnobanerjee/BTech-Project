import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import Function1 as fun
import Function2 as fun2
import xlsxwriter as xl
import numpy as np
from scipy.interpolate import CubicSpline as CS


Bigdata = []

Name = ["Anish", "Avijit", "Aneshwa", "Sayan","Shreya", "Koushik","Sudipta", "Sneha", "Moudud", "Pallabi"]

wb = xl.Workbook('F:\BT-2023_Project\Data\EDA_Peaks1.xlsx')

for k1 in range(len(Name)):
    print(k1)
    d = pd.read_excel("F:\BT-2023_Project\Data\File_PPG_EDA.xlsx",
                      sheet_name=Name[k1], header=None)
    df = pd.DataFrame(d)
    worksheet = wb.add_worksheet(Name[k1])

    # Load Raw Data:
    bnormEDA = list(df.loc[0:480000, 2])

    # Normalization:
    normEDA = fun.norm(fun.FilterE(fun.movmean(bnormEDA, 50)))

    
    EDAdata = [normEDA[30000:90000], normEDA[120000:180000], normEDA[180000:240000],normEDA[270000:330000], normEDA[330000:390000], normEDA[420000:480000]]
    
    peaks = []
    for i in range(len(EDAdata)):
        peaks.append(fun2.count_Peak_Minima_EDA(EDAdata[i])/4)

    
    Condition = ['Resting before Reading', 'Reading', 'Resting before Listening Music',
                 'Listening Music', 'Resting before Arithmetic Calculation Task', 'Arithmetic Calculation Task']
    
    for i in range(6):

        worksheet.write(0,i,Condition[i]) 
        worksheet.write(1,i,peaks[i]) 
        
        
wb.close()
