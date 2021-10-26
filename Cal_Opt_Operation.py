'''
這個函數裡面會有計算一次跟直接Thread一套性運算的的方式
'''
from threading import Thread
import random
from time import clock
import Get_Stock_Data_Save_Load as st_data

import json

import Cal_Stock_Theorem as theorem
import Cal_Stock_Decision as decision
import Cal_Stock_Identify as identify

# Result = [BaseScore,paramater]

import os
ContinueRuning = False
Base_opt_file = os.path.join(os.getcwd(),'Recipe')
if not os.path.exists(Base_opt_file):
    os.makedirs(Base_opt_file)


def Write_Optimize_Parameter_To_File(SetFileName,out):
    global Base_opt_file
    filepath = os.path.join(Base_opt_file,SetFileName)
    with open(filepath, 'w') as out_file:
        json.dump(out, out_file)

def Read_Optimize_Parameter_Form_File(ReadFileName):
    global Base_opt_file
    filepath = os.path.join(Base_opt_file, ReadFileName)
    with open(filepath, 'r') as in_file:
        your_list = json.load(in_file)
    return your_list

def MakeNormalRanDom(param,alpha):
    if type(param).__name__ == 'list':
        param = [MakeNormalRanDom(i,alpha) for i in param]
        #print( "List is true")
        return param
    elif type(param).__name__ == 'str':
        return param
    else:
        #print("SScount", SScount)
        param = random.uniform( -1*alpha , alpha)
        return param

def MakeGaussianRandom(param,alpha):
    if type(param).__name__ == 'list':
        param = [MakeGaussianRandom(i,alpha) for i in param]
        #print( "List is true")
        return param
    elif type(param).__name__ == 'str':
        return param
    else:
        #print("SScount", SScount)
        param = random.gauss(mu=param, sigma=alpha)
        return param

class Opt_Cal_Onece(Thread):
    def __init__(self,paramater = []):
        Thread.__init__(self)
        self.Paramater = paramater
        self.Throrem = theorem.Method()
        self.Decision = decision.Method()
        self.Identity = identify.Method()
        self.Result = []
        self.Cal_Datas = []
        self.Cal_History = []
        self.Rank = []
        self.BuySell = []
        self.isRunning =True
        self.Final_Score = []
        self.start()



    def __del__(self):
        del self.Paramater
        del self.Throrem
        del self.Decision
        del self.Identity
        del self.Result
        del self.Cal_Datas
        del self.Rank
        del self.BuySell
        del self.Cal_History


    def run(self):
        start = clock()
        resul_Method = self.Throrem.Method_Cal(self.Paramater)

        #print('resul_Method',resul_Method)
        self.Cal_Datas = self.Decision.Method_Cal(self.Paramater,resul_Method)
        #print("Get Avg Score", self.Decision.Method_Cal_By_Stock())
        #print('resul_Method',self.Cal_Datas)
        self.BuySell = self.Decision.BuySell
        del resul_Method
        self.Result = [self.Identity.Method_Cal(self.Paramater,self.Cal_Datas),self.Paramater]
        self.Rank = self.Identity.Ranks
        self.Final_Score = self.Identity.Final_Score
        self.Cal_History = self.Identity.History
        #print(self.Result)
        self.isRunning = False
        end = clock()
        print("Optimize one Time cost", start, ">>", end, '=', end - start)


class ThreadCalculate(Thread):
    def __init__(self,numb=0, paramater=[],alpha = 30 ,alphaDiv=1.3, \
                 alphaLimit = 0.005 ,seedCount = 30,areaSeedCount = 20 ,\
                 labelqt = ""):
        Thread.__init__(self)
        self.Number = numb
        self.Paramater = paramater
        self.Throrem = theorem.Method()
        self.Decision = decision.Method()
        self.Identity = identify.Method()
        self.Alpha = alpha
        self.Limit = alphaLimit
        self.SeedCount = seedCount
        self.BestScore = [1.0,[]] # Score and Paramater
        self.AlphaDiv = alphaDiv
        self.AreaSeedCount = areaSeedCount
        self.QTLabel = labelqt
        self.Result = []

        self.Running = True

        self.start()

    def __del__(self):
        del self.Paramater
        del self.Throrem
        del self.Decision
        del self.Identity
        del self.Alpha
        del self.Limit
        del self.Result
        del self.BestScore
        del self.SeedCount
        del self.AlphaDiv
        del self.AreaSeedCount
        del self.Number

    def run(self):
        print("Opt_Parameter",self.Paramater)
        newParam = []
        self.BestScore = [1.0, []]  # Score and Paramater

        alp = self.Alpha
        while (self.Running):
            del newParam
            newParam = []
            #生一堆Seed
            for i in range(self.SeedCount):
                newParam.append(MakeGaussianRandom(self.Paramater,alp))
            for i in range(self.AreaSeedCount):
                newParam.append(MakeNormalRanDom(self.Paramater,self.Alpha))
            newParam.append(self.Paramater)

            #計算結果
            print("is Calculateing")
            resul_Identify = []
            for parame in newParam:
                resul_Method = self.Throrem.Method_Cal(parame)
                resul_Decision = self.Decision.Method_Cal(parame, resul_Method)
                del resul_Method
                self.Identity.Method_Cal(parame, resul_Decision)
                res_Identyfy = self.Identity.Final_Score
                resul_Identify.append([res_Identyfy,parame])
                del resul_Decision

            #for i in resul_Identify:
            #    print("Optmize result ", i)

            #比較結果是不是有超過之前的結果
            haveBest = 0
            for scores in resul_Identify:
                try:
                    if(scores[0] > self.BestScore[0]):
                        haveBest = 1
                        self.BestScore = scores
                        self.Paramater = scores[1]

                except:
                    pass
            '''
            self.QTLabel.set(self.Number.__str__()+"_Alp"+alp.__str__()+\
                                     " ; Bast Score= "+self.BestScore[0].__str__())
            '''
            print(self.Number,"_Alpha",alp," ;;Bast Score",self.BestScore)
            #如果 Alpha 小於設定就停
            if alp < self.Limit:
                break

            #如果有新的最大值就放大範圍，沒得化就縮小範圍
            if haveBest == 1 :
                alp *= self.AlphaDiv
            else:
                alp /= self.AlphaDiv

        #都算完了就儲存結果
        print(self.Number," __ one Thread run finish")
        self.Running = False
        self.Result = self.BestScore
