'''
取得股票的資料原始資料
'''

import pandas as yf
#import pandas_datareader as pdr
import numpy as np
import datetime as datetime
import time

def Get_Datas(STockName=""):
    ct = time.localtime()
    end_time = datetime.datetime(ct.tm_year, ct.tm_mon, ct.tm_mday,ct.tm_hour,ct.tm_min,ct.tm_sec)
    start_time = datetime.datetime((ct.tm_year - 1), ct.tm_mon, ct.tm_mday) #Get 5 years later data until now
    print("Time Stamp ",start_time,' >>',end_time)
    Stockdatas = yf.download(STockName, start=start_time,end = end_time)
    return Stockdatas