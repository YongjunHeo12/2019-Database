# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:53:24 2019

"""
#그래프 만드는 부

def str2int(s):
    
    s = s.replace('"', '')
    s = s.replace(',','')
    return int(s)

Player2010 = dict()

KEYS =  ('Driving Distance - (ROUNDS)', 'All-Around Ranking - (EVENTS)', 'World Money List - (MONEY)', 'Total Money (Official and Unofficial) - (MONEY)')
TYPES = ('INT', 'INT', 'MONEY', 'MONEY')

with open('PGA_Data_Historical.txt') as f:
    for line in f:
        items = line.strip().split('\t')
        if len(items) != 5: continue
        if items[1] != '2010': #2010년도것만 가지고 한다는 뜻
            continue        
        player, var, val = items[0], items[3], items[4]
 
        if var in KEYS and TYPES[KEYS.index(var)] == 'MONEY':
            val = str2int(val)
            
        if player in Player2010:
            if var in Player2010[player]:
                print('Key Dup')
            else:
                Player2010[player][var] = val
        else:
            Player2010[player] = dict()
            Player2010[player][var] = val
            
print(len(Player2010))

############################### 
Player2010_1 = dict()
for player, p_dict in Player2010.items():
    tmp = []
    for k in KEYS: 
        if k in p_dict:
            tmp.append(p_dict[k])
    if len(tmp) == len(KEYS):
        Player2010_1[player] = tmp
        
print('TOTAL NUMBER of DATA====>', len(Player2010_1.keys()))        

################################
import pandas as pd
import numpy as np

# correlation
lst = list()
for key, val in Player2010_1.items(): 
    lst.append([int(x) for x in val])

df = pd.DataFrame(data=np.array(lst), columns=KEYS)
corr = df.corr(method = 'pearson')
print(corr)

#################################
import numpy as np

# Linear Regression
lst = list()
for key, val in Player2010_1.items(): 
    lst.append([int(x) for x in val])
    
data = np.array(lst)    
print(data.shape)    

x_data, y_data = data[:, :-2], data[:, -1]

from sklearn.linear_model import LinearRegression

reg = LinearRegression()
reg.fit(x_data, y_data)     # 학습

print("lr.coef_: {}".format(reg.coef_))
print("lr.intercept_: {}".format(reg.intercept_))

print("훈련 세트 점수: {:.3f}".format(reg.score(x_data, y_data)))

################################

# matplot
import matplotlib.pyplot as plt


x = data[:, 2]
y = data[:, -1]
plt.scatter(x, y, marker='o')

plt.plot()
plt.show()


