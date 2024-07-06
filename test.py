import pandas as pd

df = pd.read_csv("IRIS.csv")
jensy = []
for rows in df["sepal_width"]:
    jensy.append(type(rows))

    # print(type(rows), rows)
aditya = set(jensy)
if len(list(aditya)) == 1:
    print("COnsistent Data")
else:
    print("Inconsistent Data Type")
    print(aditya)