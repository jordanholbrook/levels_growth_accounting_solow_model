# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 20:47:34 2020

@author: jcholbro
"""


import requests 
import pandas as pd
import bs4
import re
import datetime
import numpy as np


df = pd.read_excel(r"C:\Users\jcholbro\OneDrive - University Of Houston\School_UH\Macro_1\Data/pwt91.xlsx", sheet_name='Data')


df['y'] = df['cgdpo'] / df['emp']
df['k'] = df['cn'] / df['emp']


    
df.loc[(df['countrycode']=='USA') & (df['year']==1980)].y
df.loc[(df['countrycode']=='USA') & (df['year']==1980)].k
df.loc[(df['countrycode']=='USA') & (df['year']==1980)].hc


def TFP(alpha):
    y = df.y
    k = df.k
    h = df.hc
    A = (y / (k**(alpha)*h**(1-alpha)))
    TFP = A**(1 / (1-alpha))
    df['TFP'] = TFP
TFP(1/3)

#df.loc[(df['countrycode']=='USA') & (df['year']==1980)].TFP



#This function Creates table 1 and Table 2 for whatever countries and years you want



def Level_Accounting(country1,country2, year, alpha):
    Y1 = df.loc[(df['countrycode']==country1) & (df['year']==year)].y
    K1 =  df.loc[(df['countrycode']==country1) & (df['year']==year)].k
    H1 = df.loc[(df['countrycode']==country1) & (df['year']==year)].hc
    TFP1 = df.loc[(df['countrycode']==country1) & (df['year']==year)].TFP
    Y1 = Y1.iloc[0]
    K1 = K1.iloc[0]
    H1 = H1.iloc[0]
    TFP1 = TFP1.iloc[0]
    
    Y2 = df.loc[(df['countrycode']==country2) & (df['year']==year)].y
    K2 =  df.loc[(df['countrycode']==country2) & (df['year']==year)].k
    H2 = df.loc[(df['countrycode']==country2) & (df['year']==year)].hc
    TFP2 = df.loc[(df['countrycode']==country2) & (df['year']==year)].TFP
    Y2 = Y2.iloc[0]
    K2 = K2.iloc[0]
    H2 = H2.iloc[0]
    TFP2 = TFP2.iloc[0]
    
    gap_y = np.log(Y1/Y2)
    gap_k = np.log(K1/K2)
    gap_h = np.log(H1/H2)
    gap_TFP = np.log(TFP1 / TFP2)
    cont_gap_TFP = (1-alpha)*gap_TFP
    cont_gap_K = (alpha)*gap_k
    cont_gap_h = (1-alpha)*gap_h
    
    cont_percent_TFP = abs(cont_gap_TFP / gap_y)
    cont_percent_K = abs(cont_gap_K / gap_y)
    cont_percent_h = abs(cont_gap_h / gap_y)
    table  = []
    table_row1 = {}
    table_row1['Y\L'] = Y1
    table_row1['TFP'] = TFP1
    table_row1['K\L'] = K1
    table_row1['h'] = H1
    table.append(table_row1)
    
    table_row2 = {}
    table_row2['Y\L'] = Y2
    table_row2['TFP'] = TFP2
    table_row2['K\L'] = K2
    table_row2['h'] = H2
    table.append(table_row2)
    
    table_row3 = {}
    table_row3['Y\L'] = gap_y
    table_row3['TFP'] = gap_TFP
    table_row3['K\L'] = gap_k
    table_row3['h'] = gap_h
    table.append(table_row3)
    
    table_row4 = {}
    table_row4['Y\L'] = '--'
    table_row4['TFP'] = cont_gap_TFP
    table_row4['K\L'] = cont_gap_K
    table_row4['h'] = cont_gap_h
    table.append(table_row4)
    
    table_row5 = {}
    table_row5['Y\L'] = '--'
    table_row5['TFP'] = cont_percent_TFP*100
    table_row5['K\L'] = cont_percent_K*100
    table_row5['h'] = cont_percent_h*100
    table.append(table_row5)
    
    data = pd.DataFrame(table)
    data = data.set_index([pd.Index([country1,country2,'Gap(logs)','Contribution to Gap (logs)','Contribution Percent'])])
    return data
    
df['y1'] = df['rgdpna'] / df['emp']
df['k1'] = df['rnna'] / df['emp']
def TFP_Growth(alpha):
    y = df.y1
    k = df.k1
    h = df.hc
    A = (y / (k**(alpha)*(h**(1-alpha))))
    TFP1 = A**(1 / (1-alpha))
    df['TFP1'] = TFP1
TFP_Growth(1/3)


# This function recreates table 3 for whatever country and years you want. 
def Growth_Accounting(country1, year1, year2, alpha):
    Y1 = df.loc[(df['countrycode']==country1) & (df['year']==year1)].y1
    K1 =  df.loc[(df['countrycode']==country1) & (df['year']==year1)].k1
    H1 = df.loc[(df['countrycode']==country1) & (df['year']==year1)].hc
    TFP1 = df.loc[(df['countrycode']==country1) & (df['year']==year1)].TFP1
    Y1 = Y1.iloc[0]
    K1 = K1.iloc[0]
    H1 = H1.iloc[0]
    TFP1 = TFP1.iloc[0]
    
    Y2 = df.loc[(df['countrycode']==country1) & (df['year']==year2)].y1
    K2 =  df.loc[(df['countrycode']==country1) & (df['year']==year2)].k1
    H2 = df.loc[(df['countrycode']==country1) & (df['year']==year2)].hc
    TFP2 = df.loc[(df['countrycode']==country1) & (df['year']==year2)].TFP1
    Y2 = Y2.iloc[0]
    K2 = K2.iloc[0]
    H2 = H2.iloc[0]
    TFP2 = TFP2.iloc[0]
    
    gap_y = np.log(Y1/Y2)
    gap_k = np.log(K1/K2)
    gap_h = np.log(H1/H2)
    gap_TFP = np.log(TFP1 / TFP2)
    cont_gap_TFP = (1-alpha)*gap_TFP
    cont_gap_K = (alpha)*gap_k
    cont_gap_h = (1-alpha)*gap_h
    
    cont_percent_TFP = abs(cont_gap_TFP / gap_y)
    cont_percent_K = abs(cont_gap_K / gap_y)
    cont_percent_h = abs(cont_gap_h / gap_y)
    
    
    table  = []
    

    table_row1 = {}
    table_row1['Y\L'] = Y1
    table_row1['TFP'] = TFP1
    table_row1['K\L'] = K1
    table_row1['h'] = H1
    table.append(table_row1)
    
    table_row2 = {}
    table_row2['Y\L'] = Y2
    table_row2['TFP'] = TFP2
    table_row2['K\L'] = K2
    table_row2['h'] = H2
    table.append(table_row2)
    
    table_rowg= {}
    table_rowg['Y\L'] = abs((1/(year2-year1))*gap_y)
    table_rowg['TFP'] = abs((1/(year2-year1))*gap_TFP)
    table_rowg['K\L'] = abs((1/(year2-year1))*gap_k)
    table_rowg['h'] = abs((1/(year2-year1))*gap_h)
    table.append(table_rowg)
    
    
    table_row3 = {}
    table_row3['Y\L'] = abs(gap_y)
    table_row3['TFP'] = abs(gap_TFP)
    table_row3['K\L'] = abs(gap_k)
    table_row3['h'] = abs(gap_h)
    table.append(table_row3)
    
    table_row4 = {}
    table_row4['Y\L'] = '--'
    table_row4['TFP'] = abs(cont_gap_TFP)
    table_row4['K\L'] = abs(cont_gap_K)
    table_row4['h'] = abs(cont_gap_h)
    table.append(table_row4)
    
    table_row5 = {}
    table_row5['Y\L'] = '--'
    table_row5['TFP'] = abs(cont_percent_TFP)*100
    table_row5['K\L'] = abs(cont_percent_K)*100
    table_row5['h'] = abs(cont_percent_h)*100
    table.append(table_row5)
    
    data = pd.DataFrame(table)
    data = data.set_index([pd.Index([year1,year2,'(Log) Average Growth','Gap(logs)','Contribution to Growth (logs)','Contribution to Growth - Percent'])])
    return data

# Test Cases of Various countries
# # c= Growth_Accounting('CHN',1980, 2017, (1/3))

# # r= Growth_Accounting('IRL',1980, 2017, (1/3))

# v = Growth_Accounting('MEX',1980, 2017, (1/3))

# # x = Level_Accounting('CHN','USA',1980,(1/3))
# y = Level_Accounting('MYS','USA',1980,(1/3))
# z  = Level_Accounting('MYS','USA',2017,(1/3))

# m = Level_Accounting('MEX','USA',2017,(1/3))
# m1 = Level_Accounting('MEX','USA',1980,(1/3))

# #a = Level_Accounting('IRL','USA',2017,(1/3))


