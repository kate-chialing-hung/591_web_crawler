# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:52:14 2020

@author: 117122
"""
import pandas as pd
import matplotlib.pyplot as plt
import math
import glob, os

if __name__ == '__main__':     
    df = pd.DataFrame()
#    for i in range(5): 
    os.chdir("tmp")
    for file in glob.glob("*.xlsx"): 
#    if(True): 
        partial_df = pd.read_excel(file, index_col=0)
#        df = pd.read_excel('591_output.xlsx', index_col=0)
        df = df.append(partial_df, ignore_index=True)
        
    df.to_excel('../591_output.xlsx')
#%%
    print(df.head())
    print(df['property_number'].count())
#%%
    df = df.drop_duplicates(subset=list(df.columns))
    print(df['property_number'].count())
    
    df['monthly_price'] = [ x.replace(',','') for x in df['monthly_price']]
    df[['monthly_price']] = df[['monthly_price']].astype(int)
    
#%%
    number = df.groupby(by='phone_number').count()[['property_number']]
    price = df.groupby(by='phone_number').sum()[['monthly_price']]
    cube = number.merge(price, left_on='phone_number', right_on='phone_number')
    print(cube.count())
    
#%%
    
    x = (price['monthly_price']/1000)  ##assumption: 10 months in a year the house is occupied 
    y = number['property_number']
    
    plt.figure(figsize=(5*5, 1*5), dpi=100)
    plt.scatter(x, y, alpha=0.1, s=[150 for i in range(len(x))], edgecolors='none', marker='o')
    plt.ylim(0, y.max()+1)
    plt.xlim(0, x.max()+10)
    tick = 10
    plt.title("land-lords' projected income (currently known)")
    plt.xticks([x*tick for x in range(math.ceil(x.max()/tick)+1)])
    plt.xlabel("monthly income (K NTD)")
    plt.ylabel("number of objects")
    
    plt.savefig('../591.png')
    plt.show()
    
