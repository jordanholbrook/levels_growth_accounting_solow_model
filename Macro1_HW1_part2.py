# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 13:00:00 2020

@author: jcholbro
"""


import requests 
import pandas as pd
import bs4
import re


df = pd.read_excel(r"C:\Users\jcholbro\OneDrive - University Of Houston\School_UH\Macro_1\pwt91.xlsx", sheet_name='Data')
import datetime
import numpy as np
# The Following code transforms the data set and calculates TFP

df['y'] = df['rgdpna'] / df['emp']
df['k0'] = df['rnna'] / df['emp']
def TFP_Growth(alpha):
    y = df.y
    k = df.k0
    #h = df.hc
    A = (y / (k**(alpha)))
    TFP = A**(1 / (1-alpha))
    df['TFP'] = TFP
TFP_Growth(1/3)

df['k']=df['k0'] / df['TFP'] 


 
# This Function Gets the parameter values for whatever country you choose and years
Malaysia = df.loc[df['countrycode']=='MYS']


def Parameter_function(country1, year1, year2, alpha):
    #Find n
    pop_growth1 = df.loc[(df['countrycode']==country1) & (df['year']==year1)].emp
    pop_growth2 = df.loc[(df['countrycode']==country1) & (df['year']==year2)].emp
    pop_growth1 = pop_growth1.iloc[0]
    pop_growth2 = pop_growth2.iloc[0]
    log_pop = np.log(pop_growth1/pop_growth2)
    n = abs((1/(year2-year1))*log_pop)
    # Find gamma
    TFP1 = df.loc[(df['countrycode']==country1) & (df['year']==year1)].TFP
    TFP2 = df.loc[(df['countrycode']==country1) & (df['year']==year2)].TFP
    TFP1 = TFP1.iloc[0]
    TFP2 = TFP2.iloc[0]
    gap_TFP = np.log(TFP1 / TFP2)
    gamma = abs((1/(year2-year1))*gap_TFP)
    # Find S
    s = df.loc[(df['countrycode']==country1) & (df['year'] >= year1) & (df['year'] <=year2)]['csh_i'].mean()
    #s = savings.mean()
    # Check if years are correct
    #s = df.loc[(df['countrycode']=='USA') & (df['year'] >= 1980) & (df['year'] <=2017) ][['csh_i','year']]
    delta = 0.05
    return delta,s,gamma,n
    

# Next Step is to compute Solow Prediction on K for each time period
# Then think about how to generalize this for each country

#saving_brazil= df.loc[(df['countrycode']=='BRA') & (df['year'] >= 1980) & (df['year'] <=2017) ][['xr','irr','csh_i','year']]

    
#x= Parameter_function('USA',1980, 2017, (1/3))    

country_parameters= Parameter_function('MYS',1960, 2017, (1/3))

def Steady_State(alpha):
    delta = country_parameters[0]
    s = country_parameters[1]
    gamma = country_parameters[2]
    n = country_parameters[3]
    k_steady_state = ((s) / (gamma + n + delta))**(1/(1-alpha))
    return k_steady_state
# Choose what country you want to get the Steady State Value for

Malaysia_ss = Steady_State((1/3))



# This Function creates the Solow Model Capital per effective worker Preditions for whichever years are 
# Included
def Solow_Model(country1, year1, year2, alpha):
     delta = country_parameters[0]
     s = country_parameters[1]
     gamma = country_parameters[2]
     n = country_parameters[3]
     k_0 = df.loc[(df['countrycode']==country1) & (df['year']==year1)].k
     k_0 = k_0.iloc[0]
     predictions = []
     prediction_row = {}
     prediction_row['year'] = year1
     prediction_row['k_hat'] = k_0
     #prediction_row['y_hat'] = k_0**(alpha)
     predictions.append(prediction_row)
     for year in range(year2-year1):
         prediction_row = {}
         k_t = ((((1- delta)*k_0)/((1+n)*(1+gamma))) + ((s*k_0**(alpha))/((1+n)*(1+gamma))))
         prediction_row['year'] = year1+1
         prediction_row['k_hat'] = k_t
         #prediction_row['y_hat'] = k_t**(alpha)
         k_0 = k_t
         year1 = year1+1 
         predictions.append(prediction_row)
     output = pd.DataFrame(predictions)   
     return output
# Choose what country you want to run the Solow Model Predictions on
results = Solow_Model('MYS',1980, 2017, (1/3))

# These Functions get the data for whichever country you choose and whatever years you want. 

def Actual_Data(country1, year1, year2, alpha):
    j = df.loc[(df['countrycode']==country1) & (df['year'] >= year1) & (df['year'] <=year2)][['year','k']]
    return j
# Choose what Country you want here
# act = Actual_Data('NLD',1980, 2017, (1/3))
act1= Actual_Data('MYS',1960, 2017, (1/3))

# results = pd.merge(results, act, on='year')
# results1 = pd.merge(results, act1, on='year')

# results['difference'] = abs(results['k']-results['k_hat'])

def Actual_Data1(country1, year1, year2, alpha):
    j = df.loc[(df['countrycode']==country1) & (df['year'] >= year1) & (df['year'] <=year2)][['year','emp']]
    return j

#act2= Actual_Data1('MYS',1955, 2017, (1/3))


import matplotlib.pyplot as plt
# This Generates all the Graphs in my presenation
# x = results['year']
# y1 = results['k_hat']
# plt.plot(x, y1, label="Solow Predict")
# y2 = results['k']

# plt.plot(x, y2, label="Actual")
# plt.plot(x, y2)
# # y3 = results['difference']

# # plt.plot(x, y3, label="Residual")

# plt.xlabel('Years')
# plt.ylabel('Capital Per Effective Worker')

# plt.title('Netherlands')

# plt.legend()

# plt.show()


# import matplotlib.pyplot as plt

# x = act1['year']
# #y1 = results['k_hat']
# #plt.plot(x, y1, label="Solow Predict")
# y2 = act1['k']

# # plt.plot(x, y2, label="Actual")
# plt.plot(x, y2)
# # y3 = results['difference']

# # plt.plot(x, y3, label="Residual")

# plt.xlabel('Years')
# plt.ylabel('Capital Per Effective Worker')

# plt.title('Malaysia')

# #plt.legend()

# plt.show()

# correlation = act2['emp'].corr(act['k'])

# x = act1['year']
# #y1 = results['k_hat']
# #plt.plot(x, y1, label="Solow Predict")
# y2 = act2['k']

# # plt.plot(x, y2, label="Actual")
# plt.plot(x, y2)
# # y3 = results['difference']

# # plt.plot(x, y3, label="Residual")

# plt.xlabel('Years')
# plt.ylabel('Capital Per Effective Worker')

# plt.title('Malaysia')


# correlation = act2['emp'].corr(act['k'])
# correlation1 = saving['s'].corr(act['k'])
# correlation2 = act['k'].corr(saving['s'])
# correlation3 = act['k'].corr(saving['xr'])
# correlation4 = results['k'].corr(results['k_hat'])



# saving_brazil['s'] = saving_brazil['csh_i']*10
# #plt.legend()

# plt.show()



# x = saving_brazil['year']
# y1 =act['k']

# plt.plot(x, y1, label="K/L")
# y2 = saving_brazil['csh_i']*10

# plt.plot(x, y2, label="Saving")
# plt.plot(x, y2)
# # y3 = results['difference']

# # plt.plot(x, y3, label="Residual")

# plt.xlabel('Years')
# #.ylabel('Capital Per Effective Worker')

# plt.title('Brazil')

# plt.legend()

# plt.show()

# x = saving['year']
# y1 =act['k']

# plt.plot(x, y1, label="K/L")
# y2 = saving['xr']

# plt.plot(x, y2, label="Exchange Rate")
# plt.plot(x, y2)
# # y3 = results['difference']

# # plt.plot(x, y3, label="Residual")

# plt.xlabel('Years')
# #.ylabel('Capital Per Effective Worker')

# plt.title('Malaysia')

# plt.legend()

# plt.show()



# x = act2['year']
# #y1 = results['k_hat']
# #plt.plot(x, y1, label="Solow Predict")
# y2 = act2['emp']

# # plt.plot(x, y2, label="Actual")
# plt.plot(x, y2)
# # y3 = results['difference']

# # plt.plot(x, y3, label="Residual")

# plt.xlabel('Years')
# plt.ylabel('Labor Force (Millions)')

# plt.title('Malaysia')

# #plt.legend()

# plt.show()