import pandas as pd

df = pd.read_excel("Hourly_prices_2050.xlsx")
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

print(df.loc[df.groupby('Date')['price_new'].idxmax(), 'Hour'].value_counts())
print(df.loc[df.groupby('Date')['price_new'].idxmin(), 'Hour'].value_counts())
