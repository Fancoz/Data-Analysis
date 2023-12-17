import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
# 设置正常显示符号(负号)
plt.rcParams['axes.unicode_minus'] = False


df = pd.read_excel(r'D:\workplace-py\Data_analysis\230614-16\data\旅游网站精华游记数据.xlsx')
df.head(10)

def dealplace(place): #筛选途径地点中的中文地名
    s = '' #定义一个空字符串
    if type(place)==str:
        for c in place:
            if not ((c>='a')and(c<='z'))or((c>='A')and(c<='Z')):
                s = s+c
    else:
        s = place
    return s

df['途经地点'] = df['途经地点'].apply(lambda x:dealplace(x)) # 将dealplace函数应用到‘途经地点’字段
df['途经地点'] = df['途经地点'].str.replace('途经：', '').str.replace('>', '、')
df.head(20)

def dealview(view):# 处理阅览数当中的数据
    num = view
    if type(num) == str:
        if '万' in num:
            if '.' in num:
                num = num.replace('.','').replace('万','000')
            else:
                num = num.replace('万','0000')
    return num

df['阅览数'] = df['阅览数'].apply(lambda x:dealview(x)).astype('int') #astype('int')可用于转化D对象每一列的数据类型
df.head()

df['出发日期'].str.split(expand=True) #expand=True直接将分列后的结果转换成D对象

df['出发日期'] = df['出发日期'].str.split(expand=True) [0]
df.head()

df['天数'] = df['天数'].str.slice(1, -1).astype('int') # 取天数数字
df.head()

df['人均消费（元）'] = df['人均消费（元）'].str.slice(2, -1) # 取人均消费数字
df.head()

df[df.duplicated(subset=['标题']) == True] # 只检查标题重复

df.drop_duplicates(subset=['标题'], inplace=True)
df[df.duplicated(subset=['标题']) == True] # 只检查标题重复

df.isnull().sum()

df.T.isnull().sum() # T:转置

df[df.T.isnull().sum() > 2]

'删除前的行数:' + str(len(df))

df.dropna(how='all', inplace=True) # any:存在缺失即删除, all:全部缺失即删除 | thresh:5个及以上字段有数据则保留（ thresh=5）
'删除前的后数:' + str(len(df))

series = df['天数'][df['天数'] > 15]
'删除前的行数:' + str(len(df))

df.drop(series.index, axis=0, inplace=True)
'删除后的行数:' + str(len(df))

df.to_excel(r'./旅游网站精华游记数据(预处理).xlsx')
'保存成功'

df = pd.read_excel(r'./旅游网站精华游记数据(预处理).xlsx')
df.head(10)

df['月份'] = pd.to_datetime(df['出发日期']).dt.month # 添加月份一列
df.head()

df.to_excel(r'./旅游网站精华游记数据(预处理).xlsx', index=False)

month = df.groupby('月份').size() # 按月份分组, 获得统计个数
month

plt.figure(figsize=(10, 5)) # 设置一个10*5的画布
plt.title('每月游客旅游次数折线图')
plt.xlabel('月份')
plt.xticks(range(1, 13))
plt.ylabel('旅游次数')
plt.plot(month.index, month, color='m')
for i,j in zip(range(len(month)), month):
    plt.text(i+1, j+1, j, ha='center', va='bottom')
plt.show()

plt.figure(figsize=(10, 9), dpi=80)
# 第一个子图
plt.subplot(2, 1, 1)
plt.title('按天数统计旅游次数直方图')
plt.xlabel('天数')
plt.ylabel('旅游次数')
plt.xticks(range(1, 16))
plt.hist(df['天数'], color='m', edgecolor='k')
# 第二个子图
plt.subplot(2, 1, 2)
plt.title('按人均消费统计旅游次数直方图')
plt.xlabel('人均消费(元)')
plt.ylabel('旅游次数')
plt.hist(list(df['人均消费（元）']), color='m', edgecolor='k')
plt.show()

data_label = df['旅行标签'].dropna()
data_label

label = data_label.str.split()
label

label_list = []
for i in label:
    label_list.extend(i)
label_list

df_label = DataFrame(label_list, columns=['标签'])
df_label

df_label['次数'] = 1
df_label

df_label_count = df_label.groupby('标签').agg('count').sort_values(by='次数', ascending=False).head()
df_label_count

plt.figure(figsize=(8, 6))
plt.title('游客旅游方式饼状图')
plt.pie(df_label_count['次数'], labels=df_label_count.index, autopct='%.2f%%')
plt.show()




