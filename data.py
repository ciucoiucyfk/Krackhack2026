import pandas as pd
import os
d1 = pd.read_csv('Datasets/d1.csv')
a = len(d1)
for x in os.listdir('Datasets')[1::]:
    d2 = pd.read_csv(f'Datasets/{x}')
    a += len(d2)
    d1 = pd.concat([d1,d2])
d1 = d1.drop(columns=['a','b'])

print(d1.columns)