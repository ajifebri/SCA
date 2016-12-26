from tkinter import *
from tkinter import ttk
from tkinter import font

class TableData:

    def __init__(self,parent,attributes,columns,data):
        self.parent = parent
        self.tableName = StringVar()
        self.tableName.set(attributes['tableName'])
        self.columns = columns
        self.columnCount = 0
        self.borderColor = attributes['borderColor']
        self.titleBG = attributes['titleBG']
        self.titleFG = attributes['titleFG']
        self.titleFontSize = attributes['titleFontSize']
        self.headerBG = attributes['headerBG']
        self.headerFG = attributes['headerFG']
        self.headerFontSize = attributes['headerFontSize']
        self.dataRowColor1 = attributes['dataRowColor1']
        self.dataRowColor2 = attributes['dataRowColor2']
        self.dataRowFontSize = attributes['dataRowFontSize']
        self.dataRowFG = attributes['dataRowFG']
        self.data = data
        self.tableDataFrame = ttk.Frame(self.parent)
        self.tableDataFrame.grid(row=0,column=0)
        self.initUI()

    def countColumns(self):
        cnt = 0
        for i in self.columns:
            cnt += 1

        self.columnCount = cnt

    def buildTableTitle(self):
        tableTitleFont = font.Font(size=self.titleFontSize)
        Label(self.tableDataFrame,textvariable=self.tableName,bg=self.titleBG,fg=self.titleFG,font=tableTitleFont, highlightbackground=self.borderColor,highlightthickness=2).grid(row=0,columnspan=self.columnCount,sticky=(W,E), ipady=3)

    def buildHeaderRow(self):
        colCount = 0
        tableHeaderFont = font.Font(size=self.headerFontSize)
        for col in self.columns:
            Label(self.tableDataFrame,text=col,font=tableHeaderFont,bg=self.headerBG,fg=self.headerFG,highlightbackground=self.borderColor,highlightthickness=1).grid(row=1,column=colCount,sticky=W, ipady=2, ipadx=5)
            colCount += 1

    def buildDataRow(self):
        tableDataFont = font.Font(size=self.dataRowFontSize)
        rowCount = 2
        for row in self.data:
            if rowCount % 2 == 0:
                rowColor = self.dataRowColor2
            else:
                 rowColor = self.dataRowColor1
            colCount = 0
            for col in row:
                Label(self.tableDataFrame,text=col,bg=rowColor,fg=self.dataRowFG,font=tableDataFont,highlightbackground=self.borderColor,highlightthickness=1).grid(row=rowCount,column=colCount,sticky=W,ipady=1, ipadx=5)
                colCount += 1
            rowCount += 1

    def initUI(self):
        self.countColumns()
        self.buildTableTitle()
        self.buildHeaderRow()
        self.buildDataRow()

#from tkinter import *
#from tkinter import ttk
#from tableData import TableData
#import sqlite3

root = Tk()
root.geometry('1000x400')

mainframe = ttk.Frame(root).grid(row=0,column=0)

attributes = {}
attributes['tableName'] = 'Title'
attributes['borderColor'] = 'black'
attributes['titleBG'] = '#1975D1'
attributes['titleFG'] = 'white'
attributes['titleFontSize'] = 16
attributes['headerBG'] = 'white'
attributes['headerFG'] = 'black'
attributes['headerFontSize'] = 12
attributes['dataRowColor1'] = 'white'
attributes['dataRowColor2'] = 'grey'
attributes['dataRowFontSize'] = 10
attributes['dataRowFG'] = 'black'

columns = ['Col 1', 'Column 2', 'Column 3','Column    4']

results = [('1','Key','Desc','Attribute'),('2','Key Column','Description Column','AttributeColumn')]

table = TableData(mainframe,attributes,columns,results)

root.mainloop()
