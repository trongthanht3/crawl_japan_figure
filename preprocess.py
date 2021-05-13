import pandas as pd
import re

df = pd.read_csv('data/data2.csv')
df['price'] = df['price'].apply(lambda x: re.sub(',', '', x))
# print(df['price'].apply(lambda x: re.sub(',', '', x)))
df.to_csv('data/data_final.csv',index=False)

