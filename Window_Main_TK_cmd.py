#coding=utf-8
import sys
import os
from   os.path import abspath, dirname
sys.path.append(abspath(dirname(__file__)))
import tkinter
import tkinter.filedialog
from   tkinter import *
import Fun
ElementBGArray={}  
ElementBGArray_Resize={} 
ElementBGArray_IM={} 
import math
from threading import Thread
import Get_Stock_Data_Save_Load as stk_sl
import Get_Stock_ID as stk_id
import Cal_Stock_Theorem as stk_thm
import Cal_Stock_Decision as stk_des
import Cal_Stock_Identify as stk_idn
import time
def SpinBox_24_onCommand(uiName,widgetName):
    pass
def SpinBox_25_onCommand(uiName,widgetName):
    pass
def Button_3_onCommand(uiName,widgetName):
    print("Press Read CSV")
def Button_32_onCommand(uiName,widgetName):
    print("Press Load Setting")
def Button_33_onCommand(uiName,widgetName):
    print("Press Save Setting")
def Button_34_onCommand(uiName,widgetName):
    print("Press Run")
def Button_36_onCommand(uiName,widgetName):
    print("Press Reset")
def Button_37_onCommand(uiName,widgetName):
    print("Press Stop")
def Button_35_onCommand(uiName,widgetName):
    print("Press Optmize")
def Button_38_onCommand(uiName,widgetName):
    pass
def Button_39_onCommand(uiName,widgetName):
    pass

