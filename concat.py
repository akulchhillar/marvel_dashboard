import pandas as pd
import glob

path = 'C:\Users\Akul Chhillar\Desktop\Marvel Dashboard/' # use your path
all_files = glob.glob(path+"*.xlsx")

li = []

for filename in all_files:
    df = pd.read_excel(filename)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame.to_excel("consolidated.xlsx")