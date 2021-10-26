#coding=utf-8
#import libs 
import sys
import Project1_cmd
import Project1_sty
import Fun
import os
import tkinter
from   tkinter import *
import tkinter.ttk
import tkinter.font
#Add your Varial Here: (Keep This Line of comments)
#Define UI Class
class  Project1:
    def __init__(self,root,isTKroot = True):
        uiName = self.__class__.__name__
        Fun.Register(uiName,'UIClass',self)
        self.root = root
        Fun.Register(uiName,'root',root)
        style = Project1_sty.SetupStyle()
        if isTKroot == True:
            root.title("Form1")
            Fun.CenterDlg(uiName,root,500,400)
            root['background'] = '#efefef'
        Form_1= tkinter.Canvas(root,width = 10,height = 4)
        Form_1.place(x = 0,y = 0,width = 500,height = 400)
        Form_1.configure(bg = "#efefef")
        Form_1.configure(highlightthickness = 0)
        Fun.Register(uiName,'Form_1',Form_1)
        #Create the elements of root 
        ComboBox_2_Variable = Fun.AddTKVariable(uiName,'ComboBox_2')
        ComboBox_2 = tkinter.ttk.Combobox(root,textvariable=ComboBox_2_Variable, state="readonly")
        Fun.Register(uiName,'ComboBox_2',ComboBox_2)
        ComboBox_2.place(x = 53,y = 42,width = 100,height = 20)
        ComboBox_2.configure(state = "readonly")
        ComboBox_2["values"]=['aa','bb','cc']
        ComboBox_2.current(0)
        #Inital all element's Data 
        Fun.InitElementData(uiName)
        #Add Some Logic Code Here: (Keep This Line of comments)
#Create the root of Kinter 
if  __name__ == '__main__':
    root = tkinter.Tk()
    MyDlg = Project1(root)
    root.mainloop()

