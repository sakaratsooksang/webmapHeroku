import datetime
import pandas as pd
import numpy as np

# LOADING DATA
DATE_TIME = "timestart"
DATA_URL1 = ('https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv')
DATA_URL2 = 'https://raw.githubusercontent.com/Maplub/odsample/master/20190102.csv'
DATA_URL3 = 'https://raw.githubusercontent.com/Maplub/odsample/master/20190103.csv'
DATA_URL4 = 'https://raw.githubusercontent.com/Maplub/odsample/master/20190104.csv'
DATA_URL5 = 'https://raw.githubusercontent.com/Maplub/odsample/master/20190105.csv'

def load_data(DATA_URL):
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME],format= '%d/%m/%Y %H:%M')
    return data

data1 = load_data(DATA_URL1)
data2 = load_data(DATA_URL2)
data3 = load_data(DATA_URL3)
data4 = load_data(DATA_URL4)
data5 = load_data(DATA_URL5)
data = data1.copy()
print(data)
data = data.append(
    data2, ignore_index=True).append(
        data3, ignore_index=True).append(
            data4, ignore_index=True).append(
                data5, ignore_index=True)
necess = data.keys()[1:7]
data = data[list(necess)].copy()
name = {
    list(necess)[0]:'lat',
    list(necess)[1]:'lon'
}
data.rename(name,axis=1,inplace=True)
necess = data.keys()[0:3]
data = data[list(necess)].copy()
start = datetime.datetime(2019,1,1)
stop = datetime.datetime(2019,1,6)
data = data.loc[(data['timestart']> start) & (data['timestart']< stop)]
print(data)
data.to_parquet('data.pq')