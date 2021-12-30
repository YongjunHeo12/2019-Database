# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:53:24 2019

"""
#correaltaion하는 예제

import pandas as pd
import numpy as np

pga = pd.read_csv('PGA_Data_Historical.csv')
pga2010 = pga.loc[ pga['Season'] == 2010 ]  # 2010년 Data만   내가 뽑아오고 싶은 년도의 데이터만 할 수 있음
print(pga2010.shape, pga2010.columns, pga2010.dtypes)

pga2010_1 = pga2010[ ['Player Name','Variable','Value'] ]  #2010년 데이터 중 이름 등의 값만 저장
print(pga2010_1.shape, pga2010_1.columns, pga2010_1.dtypes)
print(pga2010_1.values[:5])


for idx, row in pga2010_1.iterrows(): 
    if row['Variable'] == 'World Money List - (MONEY)' :
        print(row['Value'])

##############################

# PIVOTING....
pgaWide = pga2010_1.pivot('Player Name', 'Variable', 'Value')
print('PGA_WIDE ==>', pgaWide.shape)

##############################

KEY1 = 'Driving Distance - (ROUNDS)'
KEY2 = 'All-Around Ranking - (EVENTS)'
KEY3 = 'World Golf Ranking Points - (EVENTS)'

pgaWide1 = pgaWide[ [KEY1, KEY2, KEY3] ]
print('PGA_WIDE_1 ==>', pgaWide1.shape)
pgaWide2 = pgaWide1.dropna(how='any')   # None 데이터 삭제
print('PGA_WIDE_2 ==>',pgaWide2.shape)
print(pgaWide2.columns)
print(pgaWide2.dtypes)  
print(len(pgaWide2.index), pgaWide2.index)
pgaWide2.to_csv("OUT.csv", mode='w')


##############################

# correlation
lst = list()
for idx, row in pgaWide2.iterrows(): 
    print(row.name, '-->', row.values)
    lst.append([int(x) for x in row.values])

df = pd.DataFrame(data=np.array(lst), columns=[KEY1, KEY2, KEY3])
corr = df.corr(method = 'pearson')
print(corr)



