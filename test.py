import pandas as pd
import datetime as dt

# Sample DataFrame
data = {
    'Date': ['2023-01-15', '2023-01-30', '2023-02-10', '2023-02-25', '2023-03-05'],
    'Balance': [1000, 1500, 1700, 1600, 1800]
}
df = pd.DataFrame(data)

df['New Balance'] = df.apply(lambda row: row['Balance']*2, axis=1)

print(df)




    