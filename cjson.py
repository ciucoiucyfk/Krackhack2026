import pandas as pd
import json
import numpy as np

df = pd.read_csv("Datasets/indian_food_nutrition.csv")

a = df.to_dict(orient="records")
#a=  []
#print(df)
#for x in range(len(df)):
    #a.append(dict(df.loc[x]))

with open("Datasets/dataset.json","w") as j:
    json.dump(a,j,indent=2)


