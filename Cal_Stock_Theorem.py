'''
主要為各股的計算每個取縣。

del 方法
https://python-reference.readthedocs.io/en/latest/docs/dunderdsc/delete.html


Method_Name = 最主要的名稱
Method_Format = 股要的變數的樣式跟數量
這個部份其他Cal系列應該都差不多
'''


import Get_Stock_Data_Save_Load as st_data
from time import clock

Method_Name = ['各點加權(5日)','習慣演算','習慣演算差']
#第一個是使用在基本資料處理，第二個才是演算法要用的主體資料
Method_Format = [[[0,0,0,0,0,0],[0,0,0,0,0]],
                 [[0,0,0,0,0,0],[0]],
                 [[0,0,0,0,0,0],[0,0]]
                ]

def Index_Method_Name(name = ''):
    return Method_Format[Method_Name.index(name)]

class Method():
    global Method_Name
    def __init__(self):
        self.Paramater = []
        self.Data = []
        self.Result = []
        self.tempCal = []
        #self.Serial_Datas = []

    def __delete__(self, instance):
        del self.Paramater
        del self.Data
        del self.Result
        del self.tempCal
        #del self.Serial_Datas

    def Basic_Cal(self):
        '''
        datas = st_data.Stock_Data
        self.Data = []
        for i in datas:
            #print("Data in Oneopt Basic", i)
            #for j in range(len(self.Paramater[1][0])):
            aa = i['Open'] * self.Paramater[1][0][0]
            aa += i['High'] * self.Paramater[1][0][1]
            aa += i['Low'] * self.Paramater[1][0][2]
            aa += i['Close'] * self.Paramater[1][0][3]
            aa += i['Adj Close'] * self.Paramater[1][0][4]
            aa += i['Volume'] * self.Paramater[1][0][5]

            bb = aa.shift(-1)
            bb.fillna(method='pad', inplace=True)
            cc = bb/aa

            #print("Data in Oneopt Basic", cc)
            self.Data.append(cc)
        '''
        datas = st_data.List_Stock_Data
        self.Data = []
        for i in datas:
            sa = []
            sb = []
            sc = []
            for j in range(len(i[0])):
                aa = i[0][j] * self.Paramater[1][0][0]
                aa += i[1][j] * self.Paramater[1][0][1]
                aa += i[2][j] * self.Paramater[1][0][2]
                aa += i[3][j] * self.Paramater[1][0][3]
                aa += i[4][j] * self.Paramater[1][0][4]
                aa += i[5][j] * self.Paramater[1][0][5]

                sa.append(aa)
                sb.append(aa)
            del sb[0]
            sb.append(sa[-1])
            for k,l in zip(sa,sb):
                sc.append(l/k)
            self.Data.append(sc)

    def Method_Cal(self,paramater):
        #第一層先將基本資料作處理
        start = clock()
        self.Paramater = paramater[0]
        self.Basic_Cal()
        self.Result = []
        self.Serial_Datas = []


        if self.Paramater[0] == Method_Name[0]:  # '各點加權(5日)n'
            for i in self.Data:
                #print("eachData",i)

                self.Serial_Datas = []

                reverse_Value = i[0]

                self.Serial_Datas = i/i
                for j in range(len(self.Paramater[1][1])):
                    aa = i.shift(j)
                    aa.fillna(value=reverse_Value, inplace=True)
                    self.Serial_Datas = self.Serial_Datas * aa * self.Paramater[1][1][j]
                #print("eachData", len(self.Serial_Datas))
                self.Result.append(self.Serial_Datas)
            #print("All Result",self.Result)
            end = clock()
            print("Theorem Time cost", start, ">>", end, '=', end - start)
            return self.Result
        if self.Paramater[0] == Method_Name[1]:  # '習慣演算'
            for i in self.Data:
                self.Serial_Datas = []
                reverse_Value = i[0]
                for j in i:
                    reverse_Value = (reverse_Value * self.Paramater[1][1][0] + j) / (self.Paramater[1][1][0] +1)
                    self.Serial_Datas.append(reverse_Value)
                #print("Theorem", self.Serial_Datas)
                self.Result.append(self.Serial_Datas)
            end = clock()

            print("Theorem Time cost", start, ">>", end, '=', end - start)
            #print ("Theorem",self.Result)
            return self.Result

        if self.Paramater[0] == Method_Name[2]:  # '習慣演算差'
            for i in self.Data:
                self.Serial_Datas = []
                reverse_Value = i[0]
                reverse_Value_b = i[0]
                for j in i:
                    reverse_Value = (reverse_Value * self.Paramater[1][1][0] + j) / (self.Paramater[1][1][0] +1)
                    reverse_Value_b = (reverse_Value_b * self.Paramater[1][1][1] + j) / (self.Paramater[1][1][1] + 1)
                    self.Serial_Datas.append(reverse_Value-reverse_Value_b)
                #print("Theorem", self.Serial_Datas)
                self.Result.append(self.Serial_Datas)
            end = clock()

            print("Theorem Time cost", start, ">>", end, '=', end - start)
            #print ("Theorem",self.Result)
            return self.Result


