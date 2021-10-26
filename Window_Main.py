'''
用以搭配Pyqt做成顯示介面
'''
import sys,time,os

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow ,QListWidget ,QDoubleSpinBox,QSpinBox ,QFileDialog
from PyQt5.QtCore import *
#from PyQt5.QtGui import QWheelEvent
import math

import pandas as pd
from Frame_Main import *
from threading import Thread

import Get_Stock_Data_Save_Load as stk_sl
import Get_Stock_ID as stk_id
import Cal_Stock_Theorem as stk_thm
import Cal_Stock_Decision as stk_des
import Cal_Stock_Identify as stk_idn

import Cal_Opt_Operation as stk_opt
from PyQt5.QtChart import QChart, QChartView, QBarSet
from PyQt5 import QtChart
import time


class MainWindow(QMainWindow, Ui_MainWindow):
    class ChartView(QChartView):
        def __init__(self, chart ,DispLabel):
            super().__init__(chart)
            self.Ch = chart
            self.SerialDatas = []
            self.LB = DispLabel
            self.Rank = []
            self.Tit = []
            self.CalData = []
            self.Buys = []
            self.Dates = []
            self.Cal_History = []

        def mouseMoveEvent(self, event):
            #print("ChartView.mouseMoveEvent", event.pos().x()-self.Ch.plotArea().left(), event.pos().y())
            try:

                #self.Ch = QtCharts.QChart()
                #self.Ch.update()
                #self.Ch.plotArea().
                position  = event.pos().x()-self.chart().plotArea().left()
                Total_Pos = self.chart().plotArea().right() - self.chart().plotArea().left()
                #print(position,Total_Pos)
                ind = int((position/ Total_Pos)*(len(self.SerialDatas)-2) +0.5)
                #print("index",ind)
                out_String = ""

                #aa = self.SerialDatas
                #for s in aa[ind]:
                out_String = ind.__str__() + " == " + "%.4f" % self.SerialDatas[ind] + " : "
                try:
                    out_String +=  self.Cal_History[ind][0] + " :: " + self.Dates[ind]+' : ' +'\n'
                    for i in range(5):
                        out_String += '('+self.Rank[ind][i].__str__() + ')' +\
                                        '[' +stk_sl.Stock_index[self.Rank[ind][i]][0] + '_'+\
                                            stk_sl.Stock_index[self.Rank[ind][i]][1] + '],' + \
                                      "%.2f" % ((self.CalData[self.Rank[ind][i]][ind]-1)*100) + '_' +\
                                         self.Buys[self.Rank[ind][i]][ind]+" : "
                        if i == 1:
                            out_String += '\n'
                    try:
                        out_String += '\n' + self.Cal_History[ind].__str__()
                    except:
                        pass
                except:
                    pass
                    #out_String += self.Rank[ind][i].__str__() + ':'
                #print(self.CalData[self.Rank[ind][i]][ind])
                self.LB.setText(out_String)
                #print(self.Ch.mapToPosition(event.pos().x()))
                time.sleep(0.1)
                print("Get Mouse position",position)
            except:
                pass#print("Have error with mouse point")
            return QChartView.mouseMoveEvent(self, event)
        def SetData(self,data):
            self.SerialDatas = data
            self.Tit = data[0]
        def SetRank(self,rank,calData,buys,history=[]):
            self.Rank = rank
            self.CalData = calData
            self.Buys = buys
            self.Dates = stk_sl.List_Day_Datas
            #self.Dates += self.Dates[-1]
            #self.Dates += self.Dates[-1]
            #self.Dates += self.Dates[-1]
            #del self.Dates[0]
            #del self.Dates[0]
            #del self.Dates[0]
            self.Cal_History = history

            #print("in Drawing CalData",self.Dates)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #Get Stock Chart Names
        stk_id.Get_ID_List_form_Web()
        self.Chart_list = ["Result"]
        for i in stk_id.WarrantStock:
            self.Chart_list.append(i[1])
        self.CB_Select_Chart.addItems(self.Chart_list)

        self.CB_Method_Sel.addItems(stk_thm.Method_Name)
        self.CB_Decisin_Sel.addItems(stk_des.Method_Name)
        self.CB_Identify_Sel.addItems(stk_idn.Method_Name)

        #build Button Connection
        self.PB_Load_Stock_CSV.clicked.connect(self.Click_Load_Stock_Data_Form_CSV)
        self.PB_Load_Stock_WEB.clicked.connect(self.Click_Load_Stock_Data_Form_WEB)
        self.PB_Save_Stock_CSV.clicked.connect(self.Click_Save_Stock_Data_To_CSV)
        self.PB_Load_Conditin.clicked.connect(self.Click_Load_Condition)
        self.PB_Save_Condition.clicked.connect(self.Click_Save_Condition)
        self.PB_Run_one_time.clicked.connect(self.Click_Run_One_Time)
        self.PB_Optimize.clicked.connect(self.Click_Optimize)
        self.PB_Stop.clicked.connect(self.Click_Stop)
        self.CB_Select_Chart.currentIndexChanged.connect(self.Select_Chart_Change)
        self.PB_Reset.clicked.connect(self.Click_Reset)
        self.PB_Display_log10.clicked.connect(self.ReDrawChart)

        QueueProcessing(window=self)

        #Build Chart
        self.chart = QChart()
        self.chart_view = self.ChartView(self.chart,self.LB_Select_Display)#QtCharts.QChartView(self.chart) ##
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.SC_Main_Chart.setWidget(self.chart_view)

        self.serial = QtChart.QLineSeries()
        self.chart.addSeries(self.serial)
        self.chart.createDefaultAxes()
        #self.chart.setAnimationOptions(QChart.SeriesAnimations)



        self.BestParameter = []
        self.Chart_Result = []
        self.Caled_Datas = []
        self.Oprmize_Array = []
        self.Cal_History = []

        self.Get_Data_Form_Web_Processing = False
        self.Get_Data_Form_Web_Count = 0

        self.Chart_HaveChange = False
    def Click_Reset(self):
        self.BestParameter = []
        self.Click_Run_One_Time()

    def Click_Load_Stock_Data_Form_CSV(self):
        if self.PB_Load_Stock_CSV.isChecked():
            self.LB_Finish_Stock.setText("0")
            self.LB_Total_Stock.setText((len(stk_id.WarrantStock) - 1).__str__())
            stk_sl.Read_Stock_Data_from_csv()
            self.LB_Finish_Stock.setText((len(stk_id.WarrantStock) - 1).__str__())
            self.PB_Load_Stock_CSV.setChecked(False)
    def Click_Load_Stock_Data_Form_WEB(self):
        if self.PB_Load_Stock_WEB.isChecked():
            self.Get_Data_Form_Web_Count = 1
            stk_sl.Start_Read_Stock_Data_Form_Web()
            self.LB_Total_Stock.setText((len(stk_id.WarrantStock) - 1).__str__())
            self.Get_Data_Form_Web_Processing = True
        else:
            self.Get_Data_Form_Web_Processing = False

        #stk_sl.Read_Stock_Data_From_Web()
    def Click_Save_Stock_Data_To_CSV(self):
        stk_sl.Write_Stock_Data_to_csv()
    def Click_Load_Condition(self):
        try:
            os.makedirs(os.path.join(os.getcwd(), 'Recipe'))
        except:
            pass
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "Open Recipe File",
                                                                os.path.join(os.getcwd(), 'Recipe'),
                                                                "Process Files (*.prs)")
        if fileName_choose == "":
            return
        self.BestParameter = stk_opt.Read_Optimize_Parameter_Form_File(os.path.basename(fileName_choose))
        self.CB_Method_Sel.setCurrentText(self.BestParameter[0][0])
        self.CB_Decisin_Sel.setCurrentText(self.BestParameter[1][0])
        self.CB_Identify_Sel.setCurrentText(self.BestParameter[2][0])
        self.Click_Run_One_Time()
    def Click_Save_Condition(self):
        try:
            os.makedirs(os.path.join(os.getcwd(), 'Recipe'))
        except:
            pass
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "Open Recipe File",
                                                                os.path.join(os.getcwd(), 'Recipe'),
                                                                "Process Files (*.prs)")
        if fileName_choose == "":
            return
        stk_opt.Write_Optimize_Parameter_To_File(os.path.basename(fileName_choose),self.BestParameter)

    def Click_Run_One_Time(self):
        if len(stk_sl.Stock_Data) ==0:
            return
        if self.BestParameter ==[]:
            aa = [[self.CB_Method_Sel.currentText(), stk_thm.Index_Method_Name(self.CB_Method_Sel.currentText())],
                  [self.CB_Decisin_Sel.currentText(), stk_des.Index_Method_Name(self.CB_Decisin_Sel.currentText())],
                  [self.CB_Identify_Sel.currentText(), stk_idn.Index_Method_Name(self.CB_Identify_Sel.currentText())]]
            self.BestParameter = stk_opt.MakeNormalRanDom(aa,self.SB_Alpha.value())

            print("1st Parameter : ",self.BestParameter[0])
            print("2nd Parameter : ", self.BestParameter[1])
            print("3rd Parameter : ", self.BestParameter[2])
        self.PrintBestParameter()
        aa = stk_opt.Opt_Cal_Onece(self.BestParameter)
        for i in range(1000):
            if not aa.isRunning :
                break
            time.sleep(0.01)
        #print("Result ==",aa.Result)
        self.Chart_Result = aa.Result[0]
        self.Caled_Datas = aa.Cal_Datas
        self.Get_Rank = aa.Rank
        self.Cal_Data = aa.Cal_Datas
        self.Buys = aa.BuySell
        self.Cal_History = aa.Cal_History
        #print("in Main Cal_Datas" , self.Buys)
        self.ReDrawChart()
        self.Disp_Final_Result(aa.Final_Score)
        del aa

    def PrintBestParameter(self):
        self.LB_Status.setText(self.BestParameter[0].__str__() + '\n' +
                               self.BestParameter[1].__str__() + '\n' +
                               self.BestParameter[2].__str__())
    def Disp_Final_Result(self,Scores):
        tx = self.LB_Status.text() + '\n' + "Result = " + Scores.__str__() +"\n::"+self.Chart_Result[-1].__str__()+'\n'
        for i in self.Get_Rank[-1]:
            tx += '['+stk_id.WarrantStock[i+1][0] +'_'+ stk_id.WarrantStock[i+1][1] + ']_' + self.Buys[i][-1] +'\n'
        self.LB_Status.setText(tx)


    def Click_Optimize(self):
        '''
        搞一堆變數找種子
        算出答案後

        '''
        #建立Seed
        if self.PB_Optimize.isChecked():
            self.optProcess = Optmize_Processing(window=self)
        else:
            try:
                del self.optProcess
            except:
                pass




    def Click_Stop(self):
        if self.PB_Stop.isChecked():
            try:
                for i in self.Oprmize_Array:
                    i.Running = False
            except:
                self.PB_Stop.setChecked(False)

    def Select_Chart_Change(self):
        self.Chart_HaveChange = True
    def ReDrawChart(self):
        self.chart.removeSeries(self.serial)
        #print("Redraw Chart",self.CB_Select_Chart.currentText())


        self.serial.clear()

        if self.CB_Select_Chart.currentIndex() == 0:
            self.ChartData = [1] + self.Chart_Result
            del self.ChartData[-1]
        else:
            dat = stk_sl.Get_Stock_List_Data(self.CB_Select_Chart.currentText())
            #print(dat)
            self.ChartData = dat['Close'].to_list()
        if self.PB_Display_log10.isChecked():
            for i in range(len(self.ChartData)):
                dx= i+1
                dy= math.log10(self.ChartData[i])#[self.Select_Line.currentRow()]
                self.serial.append(dx,dy)
                #print(dx,dy)
        else:
            for i in range(len(self.ChartData)):
                dx= i+1
                dy= self.ChartData[i]#[self.Select_Line.currentRow()]
                self.serial.append(dx,dy)
                #print(dx,dy)
        self.chart.addSeries(self.serial)
        self.chart_view.SetData(self.ChartData)
        self.chart_view.SetRank(self.Get_Rank,self.Cal_Data,self.Buys,self.Cal_History)
        #self.chart.createDefaultAxes()
        #self.serial.

        #self.chart.update()
        print("Get Draw Data", self.serial)
        #
        '''
        try:
            self.chart.removeAxis(self.axis_x)
            #self.chart.removeAxis(self.axis_y)
        except:
            pass

        self.axis_x = QtChart.QValueAxis()
        self.axis_x.setTickCount(100)#len(self.ChartData))
        self.axis_x.setLabelFormat("%d")
        self.axis_x.setTitleText("Time")

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        
        self.axis_y = QtChart.QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat("%.1f")
        self.axis_y.setTitleText("Magnitude")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.serial.attachAxis(self.axis_x)
        self.serial.attachAxis(self.axis_y)
        '''


class Optmize_Processing(Thread):
    def __init__(self,window = MainWindow):
        Thread.__init__(self)
        self.ww = window
        self.start()


    def run(self):
        while self.ww.PB_Optimize.isChecked():
            seeds = []
            st = [
                [self.ww.CB_Method_Sel.currentText(),
                stk_thm.Index_Method_Name(self.ww.CB_Method_Sel.currentText())],
                [self.ww.CB_Decisin_Sel.currentText(),
                stk_des.Index_Method_Name(self.ww.CB_Decisin_Sel.currentText())],
                [self.ww.CB_Identify_Sel.currentText(),
                stk_idn.Index_Method_Name(self.ww.CB_Identify_Sel.currentText())]
            ]
            for i in range(self.ww.SB_Seed.value()):
                seeds.append(stk_opt.MakeNormalRanDom(st, self.ww.SB_Alpha.value()))
            if not self.ww.BestParameter == []:
                seeds.append(self.ww.BestParameter)

            optmize_array = []
            print('Get Seed :', seeds)
            a = 0
            # 利用多執行續將建立的Seed用Run一次的方式先Run結果
            self.ww.LB_Opt_Display_2.setText("Start Opitmize")
            try:
                for i in range(len(self.ww.Oprmize_Array)):
                    del self.ww.Oprmize_Array[0]
                # del self.Oprmize_Array
            except:
                pass

            for i in seeds:
                self.ww.Oprmize_Array.append(stk_opt.ThreadCalculate(numb = a,
                                                             paramater=i,
                                                             alpha=self.ww.SB_Alpha.value(),
                                                             alphaDiv=self.ww.SB_Alpha_Div.value(),
                                                             alphaLimit=1,
                                                             seedCount=20,
                                                             areaSeedCount=20,
                                                             labelqt=self.ww.LB_Opt_Display))
                a+=1
            # 等待Run完成
            best_Score = 0
            while self.ww.PB_Optimize.isChecked():
                all_finish = True
                numb_Count = 0
                for i in self.ww.Oprmize_Array:
                    if i.Running == True:
                        all_finish = False
                    else:
                        numb_Count +=1
                try:
                    aa = float(self.ww.LB_Opt_Display.text().split('Bast Score= ')[1])
                    if aa > best_Score:
                        best_Score = aa
                except:
                    pass

                self.ww.LB_Opt_Display_2.setText("First Step Optmize is finish by : "+ numb_Count.__str__()+\
                                                 " : "+self.ww.SB_Seed.value().__str__() + ' :: Best_Score= ' +\
                                                 "%.4f" % best_Score)
                if all_finish == True:
                    break
            if self.ww.PB_Stop.isChecked():
                self.ww.PB_Stop.setChecked(False)
                '''
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
            self.ww.LB_Opt_Display_2.setText("First Optmize is finish")
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
            while len(ss) > self.ww.SB_Group.value():
                del ss[self.ww.SB_Group.value()]
            a = 0
            for i in ss:
                self.ww.Oprmize_Array.append(stk_opt.ThreadCalculate(numb=a,
                                                                  paramater=i[1],
                                                                  alpha=self.ww.SB_Alpha.value(),
                                                                  alphaDiv=self.ww.SB_Alpha_Div.value(),
                                                                  alphaLimit=self.ww.SB_Alpha_Limit.value(),
                                                                  seedCount=self.ww.SB_Gass_Random.value(),
                                                                  areaSeedCount=self.ww.SB_Area_Random.value(),
                                                                  labelqt=self.ww.LB_Opt_Display))
                a +=1
            best_Score = 0
            while self.ww.PB_Optimize.isChecked():
                all_finish = True
                numb_Count = 0
                for i in self.ww.Oprmize_Array:
                    if i.Running == True:
                        all_finish = False
                    else:
                        numb_Count +=1
                try:
                    aa = float(self.ww.LB_Opt_Display.text().split('Bast Score= ')[1])
                    if aa > best_Score:
                        best_Score = aa
                except:
                    pass
                self.ww.LB_Opt_Display_2.setText("Scend Step Optmize is finish by : " + numb_Count.__str__() +\
                                                 " : "+self.ww.SB_Group.value().__str__() + ' :: Best Score= '\
                                                 "%.4f" % best_Score)
                if all_finish == True:
                    break

            if self.ww.PB_Stop.isChecked():
                self.ww.PB_Stop.setChecked(False)
                '''
                self.ww.PB_Optimize.setChecked(False)
                return
                # 優化完成後，在排序選最好的那個為結果
                
                '''
            temp1 = []
            for i in self.ww.Oprmize_Array:
                temp1.append(i.Result)

            ss = sorted(temp1, key=lambda temp1: temp1[0], reverse=True)
            self.ww.PB_Optimize.setChecked(False)
            self.ww.BestParameter = ss[0][1]
            self.ww.PB_Run_one_time.setChecked(True)


            #if not self.ww.PB_Stop.isChecked():
            self.ww.BestParameter = ss[0][1]
            self.ww.Click_Run_One_Time()
            self.ww.PB_Stop.setChecked(False)
            self.ww.PB_Optimize.setChecked(False)



class QueueProcessing(Thread):
    def __init__(self,window = MainWindow):
        Thread.__init__(self)
        self.daemon = True
        self.ww = window
        self.start()

    def run(self):
        while self.daemon:
            try:
                if self.ww.Get_Data_Form_Web_Processing :
                    print("Try Get Stock Data Form web",self.ww.Get_Data_Form_Web_Processing,self.ww.Get_Data_Form_Web_Count)
                    self.ww.LB_Finish_Stock.setText(self.ww.Get_Data_Form_Web_Count.__str__())
                    stk_sl.Read_Stock_Data_From_Web(self.ww.Get_Data_Form_Web_Count)
                    self.ww.Get_Data_Form_Web_Count += 1
                    if self.ww.Get_Data_Form_Web_Count >= len(stk_id.WarrantStock):
                        self.ww.Get_Data_Form_Web_Processing = False
                        self.ww.PB_Load_Stock_WEB.setChecked(False)
                        stk_sl.data_toList()
                else:
                    time.sleep(0.1)

                if self.ww.Chart_HaveChange:
                    time.sleep(0.1)
                    self.ww.ReDrawChart()
                    self.ww.Chart_HaveChange = False

            except:
                time.sleep(0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()

    sys.exit(app.exec_())

