from Window_Main_TK import *
import sys,time,os
import math
from threading import Thread

import Get_Stock_Data_Save_Load as stk_sl
import Get_Stock_ID as stk_id
import Cal_Stock_Theorem as stk_thm
import Cal_Stock_Decision as stk_des
import Cal_Stock_Identify as stk_idn
import Cal_Opt_Operation as stk_opt

from tkinter import filedialog
'''
self.ComboBox_9 =Method
self.ComboBox_10 = Decision
self.BComboBox_11 = Identify

self.Button_3 = Load CSV

self.Spinbox_13 = Seed //SeedVar
self.Spinbox_24 = Group //GropeVar
self.Spinbox_25 = Gass Rand //GassVar
self.Spinbox_26 = Area Rand //AreaVar
self.Spinbox_27 = Alpha //AlphaVar

self.Button_32 = Load
self.Button_33 = Save
self.Button_34 = Run
self.Button_38 = Optmize
self.Button_36 = Reset
self.Button_37 = Stop

example:
        self.ComboBox_9["values"] = ['ba', 'bb', 'bc']
        self.ComboBox_9.current(0)
        self.ComboBox_10["values"] = ['ca', 'cb', 'cc']
        self.ComboBox_10.current(0)
        self.BComboBox_11["values"] = ['fa', 'fb', 'fc']
        self.BComboBox_11.current(0)
        
self.Button_34.configure(command=self.Press_Button_34)

def Press_Button_34(self):
    print("at main press",self.Spinbox_27.get())
    self.InfoLabeleText.set("Change name")
    self.BestLabeleText.set("Change name1")
    self.StatusLabeleText.set("Change name2 \n next")

'''
class MyWindwo(Window_Main_TK):
    def __init__(self, parent=None):
        super(MyWindwo, self).__init__(parent)

        self.initial()

        self.BestParameter = []
        self.Oprmize_Array = []

    def initial(self):
        stk_id.Get_ID_List_form_Web()

        self.ComboBox_9["values"] = stk_thm.Method_Name
        self.ComboBox_9.current(0)
        self.ComboBox_10["values"] = stk_des.Method_Name
        self.ComboBox_10.current(0)
        self.BComboBox_11["values"] = stk_idn.Method_Name
        self.BComboBox_11.current(0)


        self.Button_3.configure(command=self.Load_CSV)
        self.Button_32.configure(command=self.Load_Param)
        self.Button_33.configure(command=self.Save_Param)
        self.Button_34.configure(command=self.RunOnece)
        self.Button_38.configure(command=self.Optimize_This)
        self.Button_36.configure(command=self.Reset_Run)
        self.Button_37.configure(command=self.Stop_Opt)

        #print(type(self.AlphaVar.get()))



    def Load_CSV(self):
        print("Load CSV")
        '''
        print("at main press", self.Spinbox_13.get())
        print("at main press", self.Spinbox_24.get())
        print("at main press", self.Spinbox_25.get())
        print("at main press", self.Spinbox_26.get())
        print("at main press", self.Spinbox_27.get())
        print(self.ComboBox_9.get())
        print(self.ComboBox_10.get())
        print(self.BComboBox_11.get())
        '''
        stk_sl.Read_Stock_Data_from_csv()

    def Load_Param(self):
        print("Load_Param")
        try:
            os.makedirs(os.path.join(os.getcwd(), 'Recipe'))
        except:
            pass

        fileName_choose = filedialog.askopenfilename( defaultextension=".prs",initialdir=os.path.join(os.getcwd(), 'Recipe'))
        if fileName_choose == '':
            return
        self.BestParameter = stk_opt.Read_Optimize_Parameter_Form_File(os.path.basename(fileName_choose))
        self.ComboBox_9.current(stk_thm.Method_Name.index(self.BestParameter[0][0]))
        self.ComboBox_10.current(stk_des.Method_Name.index(self.BestParameter[1][0]))
        self.BComboBox_11.current(stk_idn.Method_Name.index(self.BestParameter[2][0]))

        self.RunOnece()
    def Save_Param(self):
        print("Save_Param")
        try:
            os.makedirs(os.path.join(os.getcwd(), 'Recipe'))
        except:
            pass

        fileName_choose = filedialog.asksaveasfilename( defaultextension=".prs",initialdir=os.path.join(os.getcwd(), 'Recipe'))
        if fileName_choose == '':
            return
        print(fileName_choose)
        stk_opt.Write_Optimize_Parameter_To_File(os.path.basename(fileName_choose), self.BestParameter)
    def RunOnece(self):
        print("RunOnece")
        if len(stk_sl.Stock_Data) ==0:
            return
        if self.BestParameter ==[]:
            aa = [[self.ComboBox_9.get(), stk_thm.Index_Method_Name(self.ComboBox_9.get())],
                  [self.ComboBox_10.get(), stk_des.Index_Method_Name(self.ComboBox_10.get())],
                  [self.BComboBox_11.get(), stk_idn.Index_Method_Name(self.BComboBox_11.get())]]
            self.BestParameter = stk_opt.MakeNormalRanDom(aa,int(self.AlphaVar.get()))

        print("1st Parameter : ",self.BestParameter[0])
        print("2nd Parameter : ", self.BestParameter[1])
        print("3rd Parameter : ", self.BestParameter[2])
        self.PrintBestParameter()
        aa = stk_opt.Opt_Cal_Onece(self.BestParameter)
        for i in range(1000):
            if not aa.isRunning :
                break
            time.sleep(0.01)
        print("Result ==",aa.Result)
        self.Chart_Result = aa.Result[0]
        self.Caled_Datas = aa.Cal_Datas
        self.Get_Rank = aa.Rank
        self.Cal_Data = aa.Cal_Datas
        self.Buys = aa.BuySell
        self.Cal_History = aa.Cal_History
        #print("in Main Cal_Datas" , self.Buys)
        #self.ReDrawChart()
        self.Disp_Final_Result(aa.Final_Score)
        del aa
    def PrintBestParameter(self):
        print("print Best Parameter")
        self.StatusLabeleText.set(self.BestParameter[0].__str__() + '__' +
                               self.BestParameter[1].__str__() + '__' +
                               self.BestParameter[2].__str__())
    def Disp_Final_Result(self,Scores):
        print("Disp_Final_Result")
        tx = self.StatusLabeleText.get() + '\n' + "Result = " + Scores.__str__() + "\n::" + self.Chart_Result[
            -1].__str__() + '\n'
        for i in self.Get_Rank[-1]:
            tx += '[' + stk_sl.Stock_index[i ][0] + '_' + stk_sl.Stock_index[i ][1] + ']_' + self.Buys[i][
                -1] + '\n'
        self.StatusLabeleText.set(tx)
    def Optimize_This(self):
        print("Optimize")
        while True:
            seeds = []
            st = [
                [self.ComboBox_9.get(),
                 stk_thm.Index_Method_Name(self.ComboBox_9.get())],
                [self.ComboBox_10.get(),
                 stk_des.Index_Method_Name(self.ComboBox_10.get())],
                [self.BComboBox_11.get(),
                 stk_idn.Index_Method_Name(self.BComboBox_11.get())]
            ]

            for i in range(int(self.SeedVar.get())):
                seeds.append(stk_opt.MakeNormalRanDom(st, int(self.AlphaVar.get())))
            if not self.BestParameter == []:
                seeds.append(self.BestParameter)

            optmize_array = []
            print('Get Seed :', seeds)
            a = 0
            # 利用多執行續將建立的Seed用Run一次的方式先Run結果
            self.BestLabeleText.set("Start Opitmize")
            try:
                for i in range(len(self.Oprmize_Array)):
                    del self.Oprmize_Array[0]
                # del self.Oprmize_Array
            except:
                pass
            #建立一堆Thread 然後初次run一輪後在選比較好的繼續run
            for i in seeds:
                self.Oprmize_Array.append(stk_opt.ThreadCalculate(numb=a,
                                                                     paramater=i,
                                                                     alpha=self.AlphaVar.get(),
                                                                     alphaDiv=1.5,
                                                                     alphaLimit=int(self.AlphaVar.get() / 5),
                                                                     seedCount=int(
                                                                         self.GassVar.get() * 1.5),
                                                                     areaSeedCount=int(
                                                                         self.AreaVar.get() * 1.5),
                                                                     labelqt=self.InfoLabeleText))
                a += 1
            # 等待Run完成
            best_Score = 0
            while True:
                all_finish = True
                numb_Count = 0
                for i in self.Oprmize_Array:
                    if i.Running == True:
                        all_finish = False
                    else:
                        numb_Count += 1
                self.InfoLabeleText.set("Finished Process" + numb_Count.__str__())
                try:
                    aa = float(self.InfoLabeleText.get().split('Bast Score= ')[1])
                    if aa > best_Score:
                        best_Score = aa
                except:
                    pass

                self.BestLabeleText.set("First Step Optmize is finish by : " + numb_Count.__str__() + \
                                           " : " + self.SeedVar.get().__str__() + ' :: Best_Score= ' + \
                                           "%.4f" % best_Score)
                if all_finish == True:
                    break
            '''
            if self.ww.PB_Stop.isChecked():
                self.ww.PB_Stop.setChecked(False)

                self.ww.PB_Optimize.setChecked(False)

                try:
                    for i in range(len(self.ww.Oprmize_Array)):
                        del self.ww.Oprmize_Array[0]
                except:
                    pass
                return
                '''
            # 將run完的結果提出後排序
            print("All Optmize is finish")
            self.BestLabeleText.set("First Optmize is finish")
            temp1 = []
            for i in self.Oprmize_Array:
                temp1.append(i.Result)

            ss = sorted(temp1, key=lambda temp1: temp1[0], reverse=True)

            # 將獨立Thread的都砍掉
            '''
            for i in ss:
                print("Sorted Result",i)
            for i in range(len(optmize_array)):
                del optmize_array[0]
            '''
            try:
                for i in range(len(self.Oprmize_Array)):
                    del self.Oprmize_Array[0]
                # del self.Oprmize_Array
            except:
                pass
                # del self.Oprmize_Array

            self.Oprmize_Array2 = []
            # 取Group的數值，然後將這幾個重新做優化
            '''
            while len(ss) > self.GropeVar.get():
                del ss[self.GropeVar.get()]
            '''
            ss = ss[:self.GropeVar.get()]
            a = 0
            print("Start Process Scend Step")
            self.BestLabeleText.set("Start Process Scend Step")
            for i in ss:
                self.Oprmize_Array2.append(stk_opt.ThreadCalculate(numb=a,
                                                                     paramater=i[1],
                                                                     alpha=self.AlphaVar.get(),
                                                                     alphaDiv=1.5,
                                                                     alphaLimit=0.005,
                                                                     seedCount=self.GassVar.get(),
                                                                     areaSeedCount=self.AreaVar.get(),
                                                                     labelqt=self.InfoLabeleText))
                a += 1
            best_Score = 0
            while True:
                all_finish = True
                numb_Count = 0
                for i in self.Oprmize_Array2:
                    if i.Running == True:
                        all_finish = False
                    else:
                        numb_Count += 1
                self.InfoLabeleText.set("Finished Process" + numb_Count.__str__())
                #顯示最好的結果，但是好像沒啥用..因為資料傳不出來...
                try:
                    aa = float(self.BestLabeleText.get().split('Bast Score= ')[1])
                    if aa > best_Score:
                        best_Score = aa
                except:
                    pass
                self.BestLabeleText.set("Scend Step Optmize is finish by : " + numb_Count.__str__() + \
                                               " : " + self.GropeVar.get().__str__() + ' :: Best Score= ' \
                                                                                            "%.4f" % best_Score)
                if all_finish == True:
                    break
            print("Finish Process Scend")
            self.BestLabeleText.set("Finish Process Scend Step")
            '''
            if self.ww.PB_Stop.isChecked():
                self.ww.PB_Stop.setChecked(False)

                self.ww.PB_Optimize.setChecked(False)
                return
                # 優化完成後，在排序選最好的那個為結果

                '''
            temp1 = []
            for i in self.Oprmize_Array2:
                temp1.append(i.Result)

            ss = sorted(temp1, key=lambda temp1: temp1[0], reverse=True)
            # self.ww.PB_Optimize.setChecked(False)
            self.BestParameter = ss[0][1]
            # self.ww.PB_Run_one_time.setChecked(True)

            # if not self.ww.PB_Stop.isChecked():
            # self.ww.BestParameter = ss[0][1]
            self.RunOnece()
            # self.ww.PB_Stop.setChecked(False)
            # self.ww.PB_Optimize.setChecked(False)
            break

    def Reset_Run(self):
        print("Reset_Run")
        self.BestParameter = []
        self.RunOnece()
    def Stop_Opt(self):
        print("Stop_Opt")
        try:
            for i in self.Oprmize_Array:
                i.Running = False
        except:
            pass

#目前Optimize 的Thread沒有用處...因為夠塊所以直接在上面式子內處理了...
class Optmize_Processing(Thread):
    def __init__(self, window=MyWindwo):
        Thread.__init__(self)
        self.ww = window
        self.start()

    def run(self):
        while True:
            seeds = []
            st = [
                [[self.ww.ComboBox_9.get(), stk_thm.Index_Method_Name(self.ww.ComboBox_9.get())],
                 [self.ww.ComboBox_10.get(), stk_des.Index_Method_Name(self.ww.ComboBox_10.get())],
                 [self.ww.BComboBox_11.get(), stk_idn.Index_Method_Name(self.ww.BComboBox_11.get())]]
            ]
            for i in range(int(self.ww.SeedVar.get())):
                seeds.append(stk_opt.MakeNormalRanDom(st, int(self.ww.AlphaVar.get())))
            if not self.ww.BestParameter == []:
                seeds.append(self.ww.BestParameter)

            optmize_array = []
            print('Get Seed :', seeds)
            a = 0
            # 利用多執行續將建立的Seed用Run一次的方式先Run結果
            self.ww.BestLabeleText.set("Start Opitmize")
            try:
                for i in range(len(self.ww.Oprmize_Array)):
                    del self.ww.Oprmize_Array[0]
                # del self.Oprmize_Array
            except:
                pass

            for i in seeds:
                self.ww.Oprmize_Array.append(stk_opt.ThreadCalculate(numb=a,
                                                                     paramater=i,
                                                                     alpha=self.ww.AlphaVar.get(),
                                                                     alphaDiv=1.5,
                                                                     alphaLimit=int(self.ww.AlphaVar.get() / 5),
                                                                     seedCount=int(
                                                                         self.ww.GassVar.get() * 1.5),
                                                                     areaSeedCount=int(
                                                                         self.ww.AreaVar.get() * 1.5),
                                                                     labelqt=self.ww.InfoLabeleText))
                a += 1
            # 等待Run完成
            best_Score = 0
            while True:
                all_finish = True
                numb_Count = 0
                for i in self.ww.Oprmize_Array:
                    if i.Running == True:
                        all_finish = False
                    else:
                        numb_Count += 1
                try:
                    aa = float(self.ww.InfoLabeleText.get().split('Bast Score= ')[1])
                    if aa > best_Score:
                        best_Score = aa
                except:
                    pass

                self.ww.BestLabeleText.set("First Step Optmize is finish by : " + numb_Count.__str__() + \
                                                 " : " + self.ww.SB_Seed.value().__str__() + ' :: Best_Score= ' + \
                                                 "%.4f" % best_Score)
                if all_finish == True:
                    break
            '''
            if self.ww.PB_Stop.isChecked():
                self.ww.PB_Stop.setChecked(False)
                
                self.ww.PB_Optimize.setChecked(False)

                try:
                    for i in range(len(self.ww.Oprmize_Array)):
                        del self.ww.Oprmize_Array[0]
                except:
                    pass
                return
                '''
            # 將run完的結果提出後排序
            print("All Optmize is finish")
            self.ww.BestLabeleText.set("First Optmize is finish")
            temp1 = []
            for i in self.ww.Oprmize_Array:
                temp1.append(i.Result)

            ss = sorted(temp1, key=lambda temp1: temp1[0], reverse=True)

            # 將獨立Thread的都砍掉
            '''
            for i in ss:
                print("Sorted Result",i)
            for i in range(len(optmize_array)):
                del optmize_array[0]
            '''
            try:
                for i in range(len(self.ww.Oprmize_Array)):
                    del self.ww.Oprmize_Array[0]
                # del self.Oprmize_Array
            except:
                pass
                # del self.Oprmize_Array

            self.ww.Oprmize_Array = []
            # 取Group的數值，然後將這幾個重新做優化
            while len(ss) > self.ww.GropeVar.get():
                del ss[self.ww.GropeVar.get()]
            a = 0
            for i in ss:
                self.ww.Oprmize_Array.append(stk_opt.ThreadCalculate(numb=a,
                                                                     paramater=i[1],
                                                                     alpha=self.ww.AlphaVar.get(),
                                                                     alphaDiv=1.5,
                                                                     alphaLimit=0.005,
                                                                     seedCount=self.ww.GassVar.get(),
                                                                     areaSeedCount=self.ww.AreaVar.get(),
                                                                     labelqt=self.ww.InfoLabeleText))
                a += 1
            best_Score = 0
            while True:
                all_finish = True
                numb_Count = 0
                for i in self.ww.Oprmize_Array:
                    if i.Running == True:
                        all_finish = False
                    else:
                        numb_Count += 1
                try:
                    aa = float(self.ww.BestLabeleText.get().split('Bast Score= ')[1])
                    if aa > best_Score:
                        best_Score = aa
                except:
                    pass
                self.ww.BestLabeleText.setText("Scend Step Optmize is finish by : " + numb_Count.__str__() + \
                                                 " : " + self.ww.SB_Group.value().__str__() + ' :: Best Score= ' \
                                                                                              "%.4f" % best_Score)
                if all_finish == True:
                    break
            '''
            if self.ww.PB_Stop.isChecked():
                self.ww.PB_Stop.setChecked(False)
                
                self.ww.PB_Optimize.setChecked(False)
                return
                # 優化完成後，在排序選最好的那個為結果

                '''
            temp1 = []
            for i in self.ww.Oprmize_Array:
                temp1.append(i.Result)

            ss = sorted(temp1, key=lambda temp1: temp1[0], reverse=True)
            #self.ww.PB_Optimize.setChecked(False)
            self.ww.BestParameter = ss[0][1]
            #self.ww.PB_Run_one_time.setChecked(True)

            # if not self.ww.PB_Stop.isChecked():
            #self.ww.BestParameter = ss[0][1]
            self.ww.RunOnece()
            #self.ww.PB_Stop.setChecked(False)
            #self.ww.PB_Optimize.setChecked(False)


if  __name__ == '__main__':
    root = tkinter.Tk()
    MyDlg = MyWindwo(root)#Window_Main_TK(root)
    root.mainloop()