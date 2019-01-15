import urllib.request
import pandas as pd

Stock_list = ['000001', '000002', '000004','000005', '000006','000007', '000008','000009', '000010', '000011']
'''
贵州茅台　600519 
美利云   000815 
东方钽业　000962　
鹏起科技  600614 
黑芝麻    000716 
沈阳化工  000698 
中兴通讯  000063 
古井贡酒  000596
'''
Stock_list2 = ['600519', '000815', '000962', '600614', '000716', '000698', '000063', '000596']


for i in Stock_list2:
    if i.startswith('0'):
        url = 'http://quotes.money.163.com/service/chddata.html?code=1' + i + '&start=20020101&end=20190111&fields=TCLOSE;TOPEN'
    else:
        url = 'http://quotes.money.163.com/service/chddata.html?code=0' + i + '&start=20020101&end=20190111&fields=TCLOSE;TOPEN'
    print(url)
    a = urllib.request.urlretrieve(url, "./" + i + '.csv')
    # print(a)
t = 0
for i in Stock_list2:
    print(i)
    csv_temp = pd.read_csv(i+'.csv', encoding='EUC-CN')

    if t == 0:
        csv_temp.rename(columns={'收盘价': i + '_close', '开盘价': i + '_open', '日期': 'Date'}, inplace=True)
        csv_temp.drop(['股票代码', '名称', ], axis=1, inplace=True)
        # print(csv_temp[i+ '_open'])
        csv = csv_temp
    else:
        csv_temp.rename(columns={'收盘价': i + '_close', '开盘价': i + '_open'}, inplace=True)
        csv_temp.drop(['股票代码', '名称', '日期',], axis=1, inplace=True)
        # print(csv_temp[i + '_open'])
        csv = pd.concat([csv, csv_temp], axis=1)
    t += 1

csv = csv.sort_index(ascending=False)
columns = csv.columns

columns = [j for j in columns]
# print(columns)
# print(len(columns))
for j in range(int(len(columns)/2)):
    columns[2*j+1], columns[2*j+2] = columns[2*j+2], columns[2*j+1]
# print(columns)

csv = csv.loc[:,columns]
csv.to_csv('A_Stock2.csv', index=False)
