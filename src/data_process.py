import os
import pandas as pd

# ===stock data===
# 导入数据
os.chdir('/home/shensir/Documents/MyPrograming/Python/PycharmProject/MySpider/Stock/src')
df = pd.read_csv('../data/stock_data.csv')

# 格式
df.index = df['date'].apply(pd.to_datetime)
df['year'] = df.index.year
df = df[(df['year'] <= 2015)&(df['year'] >= 1992)]
df.drop(['date'], axis=1, inplace=True)

# 转化为季度数据
df = df.to_period('Q')
df = df.groupby(df.index).mean()
df.head()

# 选取要使用的变量
df = df[['year', 'close', 'trade_times', 'trade_money']]

# 保存数据
df.to_csv('../data/stock_processed.csv')


# ===gdp data===
df2 = pd.read_excel('../data/gdp_q4.xls')
df2 = df2.transpose()
df2 = df2.iloc[::-1]
df2.index = df.index

# change[手算，无季节调整，同比]
df2['gdp_rate'] = df2[[0]]
df2.columns = ['gdp', 'gdp_rate']

for i in range(0, df2.shape[0]):
    if i > 3:
        df2.iloc[i, 1] = (df2.iloc[i, 0] - df2.iloc[i-4, 0]) / df2.iloc[i-4, 0]
    else:
        df2.iloc[i, 1] = 0.25


df2.head()
df2.to_csv('../data/gdp_q4_processed.csv')

