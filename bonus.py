from tkinter import * 
from tkinter.ttk import Frame, Button, Style
from tkinter.ttk import Entry
from point import calculateBonus
import os.path

from parameters_bonus import *

# To Do:
# 1. Refactoring code supaya extensible (ganti jumlah hari, ganti jumlah karyawan).
# 2. Buat label jumlah mobil uneditable. Buat list baru untuk entries
# 3. Background entries putih-biru muda-putih

class GUI(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.pointMode = True
        self.points = [] # StringVar for entries
        self.pointsEntries = [] # List of entries
        self.carsEntries = [] # StringVar for number of cars
        self.savePoints = [] # List
        self.carsPoints = [] # List of number of cars
        self.bonuses = [] # List of bonuses
        self.parent = parent
        self.changeLabel = StringVar()
        self.totalCarsLabel = StringVar()
        self.totalPointsLabel = []
        self.initUI()


    def center(self):
        self.parent.update_idletasks()
        w = self.parent.winfo_screenwidth()
        h = self.parent.winfo_screenheight()
        size = tuple(int(_) for _ in self.parent.geometry().split('+')[0].split('x'))
        
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        self.parent.geometry("%dx%d+%d+%d" %(size + (x, y)))

    def copy(self, day):
        if self.pointMode == True:
            cars = self.carsEntries[day].get()
            for empl in range(numEmployees):
                self.points[empl][day].set(cars)

    def calculate(self):
        if self.pointMode == True:
            for day in range(numDays):
                bonuses = []
                for employee in range(numEmployees):
                    point = int(self.points[employee][day].get())
                    bonuses.append(point)
                    self.savePoints[employee][day] = point

                bonusList = list(calculateBonus(bonuses))

                for employee in range(numEmployees):
                    self.points[employee][day].set(bonusList[employee])

                    # save bonuses
                    self.bonuses[employee][day] = bonusList[employee]

            # Change mode and label
            self.pointMode = False

            self.changeLabel.set('Menampilkan Bonus')

            self.setTotalLabels()

            # Make uneditable
            self.makeEditable(False)

    def makeEditable(self, edit):
        for employee in range(numEmployees):
            for day in range(numDays):
                if edit == True:
                    self.pointsEntries[employee][day].configure(state=NORMAL)
                else:
                    self.pointsEntries[employee][day].configure(state=DISABLED)

    def pointsToFile(self, filename):
        if self.pointMode == True:
            # save points from entries
            for day in range(numDays):
                # save cars points list
                self.carsPoints[day] = int(self.carsEntries[day].get())
                for employee in range(numEmployees):
                    point_entry = self.points[employee][day].get()
                    if point_entry == '':
                        point = 0
                    else:
                        point = int(point_entry)
                    self.savePoints[employee][day] = point
            # Set total labels
            self.setTotalLabels()

            with open(filename, 'w+') as out:
                # save cars points
                for day in range(numDays-1):
                    out.write(str(self.carsPoints[day]) + ',')
                out.write(str(self.carsPoints[-1]) + '\n')

                # save employees' points
                for employeeList in self.savePoints:
                    for point in employeeList[:-1]:
                        out.write(str(point) + ',')
                    out.write(str(employeeList[-1]) + '\n')

    def setTotalLabels(self): 
        # Total cars label
        self.totalCarsLabel.set(str(sum(self.carsPoints)))

        # Total points label
        if self.pointMode == True:
            for empl in range(numEmployees):
                self.totalPointsLabel[empl].set(str(sum(self.savePoints[empl])))
        else:
            for empl in range(numEmployees):
                self.totalPointsLabel[empl].set(str(sum(self.bonuses[empl])))

    def loadPoints(self, filename):
        with open(filename, 'r') as inFile:
            line = inFile.readline()
            strLine = line.rstrip('\n').split(',')
            for strPoint in strLine:
                self.carsPoints.append(int(strPoint))

            for employee in range(numEmployees):
                line = inFile.readline()
                if line:
                    strPoints = line.rstrip('\n').split(',')
                    self.savePoints.append([int(strP) for strP in strPoints[:numDays]])
                else:
                    self.savePoints.append([0 for _ in range(numDays)])

        # Set total labels
        self.setTotalLabels()

    def bonusToFile(self, filename):
        if self.pointMode == False:
            with open(filename, 'w+') as out:

                # save employees' bonuses
                for employeeBonus in self.bonuses:
                    for dayBonus in employeeBonus[:-1]:
                        out.write(str(dayBonus) + ',')
                    out.write(str(employeeBonus[-1]) + '\n')

    def seePoint(self):
        for employee in range(numEmployees):
            for day in range(numDays):
                point = self.savePoints[employee][day]
                self.points[employee][day].set(point)
        self.pointMode = True
        self.changeLabel.set('Menampilkan Point')

        # Set total label
        self.setTotalLabels()

        # Make editable
        self.makeEditable(True)

    def seeCarsPoints(self):
        for day in range(numDays):
            point = self.carsPoints[day]
            self.carsEntries[day].set(point)

        # Set total labels
        self.setTotalLabels()

    def initUI(self):
        self.parent.title("Cuci Mobil dan Salon Mobil SCA")

        self.parent.resizable(width=False, height=False)

        Style().configure("TButton", padding=(0, 5, 0, 5),
                font='serif 10')

        num_rows = numEmployees + 5
        num_columns = numDays + 2
        for row in range(num_rows):
            self.rowconfigure(row, pad=3)

        for col in range(num_columns):
            self.columnconfigure(col, pad=3)

        title = Label(self, bg='#154360', fg='white', text="Penghitungan Poin SCA")
        title.config(font=20)
        title.grid(row=0, columnspan=num_columns, sticky=W+E)

        # Days
        for day in range(numDays):
            strDay = workDays[day]
            lbl = Label(self, text=strDay, bg='green')
            lbl.grid(row=1, column=day+1, sticky='ew', padx=3)

        # Total
        lbl = Label(self, text="Total", bg='green')
        lbl.grid(row=1, column=num_columns-1, sticky='ew')

        # Number of cars
        lbl = Label(self, text="Jumlah Mobil", bg='red')
        lbl.grid(row=2, column=0, sticky='ew')

        width_entry = 7
        for i in range(numDays):
            enText = StringVar()
            en = Entry(self, textvariable=enText, width=width_entry)
            en.grid(row=2, column=i+1)
            self.carsEntries.append(enText)

        # Copy Button
        copyButtons = []
        for col in range(1, numDays+1):
            cpyButton = Button(self, text="Copy", width=5, command=lambda col=col: self.copy(col-1))
            cpyButton.grid(row=3, column=col)
            copyButtons.append(cpyButton)

        # Employees
        for empl in range(numEmployees):
            emplRow = empl+4

            name = employees[empl]
            lbl = Label(self, text=name, bg='yellow')
            lbl.grid(row=emplRow, column=0, sticky='ew')

            emplPoint = []
            entryPoint = []
            for col in range(numDays):
                entryText = StringVar()
                pt = Entry(self, textvariable=entryText, width=width_entry)
                pt.grid(row=emplRow, column=col+1)
                emplPoint.append(entryText)
                entryPoint.append(pt)

            self.points.append(emplPoint)
            self.pointsEntries.append(entryPoint)

            # Total labels
            self.totalPointsLabel.append(StringVar())
            lblTotal = Label(self, textvariable=self.totalPointsLabel[empl], width=width_entry, bg='#FEF5E7')
            lblTotal.grid(row=emplRow, column=num_columns-1, sticky='ew')

        # Check if points file exists
        if os.path.isfile(points_file):
            self.loadPoints(points_file)
        else:
            self.savePoints = [[0 for _ in range(numDays)] for _ in range(numEmployees)]
            self.carsPoints = [0 for _ in range(numDays)]

        # Display the points
        self.seePoint()

        # Display the cars
        self.seeCarsPoints()

        
        # See the Point Button
        seePointButton = Button(self, text="Lihat Poin", command=self.seePoint)
        seePointButton.grid(row=num_rows-1, column=1, columnspan=2)

        # Save Button
        saveButton = Button(self, text="Simpan Poin", command=lambda: self.pointsToFile(points_file))
        saveButton.grid(row=num_rows-1, column=3, columnspan=2)

        # Calculate Button
        calcButton = Button(self, text="Hitung Bonus", command=self.calculate)
        calcButton.grid(row=num_rows-1, column=5, columnspan=2)

        # Save Bonus Button
        saveBonusButton = Button(self, text="Simpan Bonus", command=lambda: self.bonusToFile(bonuses_file))
        saveBonusButton.grid(row=num_rows-1, column=7, columnspan=2)

        # Label Mode
        lblMode = Label(self, textvariable=self.changeLabel, bg='yellow')
        lblMode.grid(row=num_rows-1, column=9, columnspan=2)
        self.changeLabel.set('Menampilkan Poin')

        # Total Mode
        lblSumCars = Label(self, textvariable=self.totalCarsLabel, width=width_entry, bg='#FEF5E7')
        lblSumCars.grid(row=2, column=num_columns-1, sticky='ew')
        #for row in range(numEmployees+1):

        # Initialize bonuses
        self.bonuses = [[0 for _ in range(numDays)] for _ in range(numEmployees)]


        self.pack()
        self.center()

def main():

    root = Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
