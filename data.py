import pandas as pd
import os
import numpy as np
d1 = pd.read_csv('Datasets/d1.csv')
d1 = d1.drop(columns=['b','a'])
print(d1)
a = len(d1)
for x in os.listdir('Datasets')[1:-1:]:
    d2 = pd.read_csv(f'Datasets/{x}')    
    print(d2)
    d2 = d2.drop(columns=['b','a'])
    a += len(d2)
    d1 = pd.concat([d1,d2])
    

#d1['Sno'] = np.arange(len(d1))
d1 = d1.reset_index(drop = True)
d1.to_csv("Datasets/ds.csv")
#d = pd.read_csv("Datasets/ds.csv")
#(d.drop(columns=['s'])).to_csv("Datasets/ds.csv")

#print(d1.columns)