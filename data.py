import pandas as pd

df = pd.read_csv("Datasets/ds.csv")

clean_df = df[[
    "food",
    "Protein",
    "Carbohydrates",
    "Fat",
    "Caloric Value"
]]

clean_df.columns = ["food_name", "protein", "carbs", "fat", "calories"]

clean_df.to_csv("Datasets/reduceddf.csv", index=False)