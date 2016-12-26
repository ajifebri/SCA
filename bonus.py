from tkinter import * 
from tkinter.ttk import Frame, Button, Style
from tkinter.ttk import Entry
from point import calculateBonus

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.num_cars = []
        self.pointMode = True
        self.points = []
        self.savePoints = []
        self.bonuses = []
        self.parent = parent
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
        #print(self.num_cars[day].get())
        cars = self.num_cars[day].get()
        for empl in range(8):
            self.points[empl][day].set(cars)

    def calculate(self):
        num_days = 1
        num_employees = 8
        for day in range(num_days):
            bonuses = []
            for employee in range(num_employees):
                point = int(self.points[employee][day].get())
                bonuses.append(point)
                self.savePoints[employee][day] = point

            bonusList = list(calculateBonus(bonuses))

            for employee in range(num_employees):
                self.points[employee][day].set(bonusList[employee])


    def initUI(self):
        self.parent.title("Cuci Mobil dan Salon Mobil SCA")

        self.parent.resizable(width=False, height=False)

        Style().configure("TButton", padding=(0, 5, 0, 5),
                font='serif 10')

        num_rows = 15
        num_columns = 16
        for row in range(num_rows):
            self.rowconfigure(row, pad=3)

        for col in range(num_columns):
            self.columnconfigure(col, pad=3)

        title = Label(self, bg='blue', fg='white', text="Penghitungan Poin SCA")
        title.grid(row=0, columnspan=num_columns, sticky=W+E)

        days = ["Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu", "Senin", 
                "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu", "Senin"]

        #days = ["Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu", "Senin"]
                

        employees = ["Wahyu", "Suras", "Surya", "Agung", "Nur", "Mega", "Ari", "Nando"]

        # Days
        for day in range(len(days)):
            strDay = days[day]
            lbl = Label(self, text=strDay, bg='green')
            lbl.grid(row=1, column=day+1, sticky='ew', padx=3)

        # Total
        lbl = Label(self, text="Total", bg='green')
        lbl.grid(row=1, column=num_columns-1)

        # Number of cars
        lbl = Label(self, text="Jumlah Mobil", bg='red')
        lbl.grid(row=2, column=0, sticky='ew')

        width_entry = 7
        for i in range(len(days)):
            en = Entry(self, width=width_entry)
            en.grid(row=2, column=i+1)
            self.num_cars.append(en)

        # Copy Button
        copyButtons = []
        for col in range(1, len(days)+1):
            cpyButton = Button(self, text="Copy", width=5, command=lambda col=col: self.copy(col-1))
            cpyButton.grid(row=3, column=col)
            copyButtons.append(cpyButton)

        # Employees
        for empl in range(len(employees)):
            emplRow = empl+4

            name = employees[empl]
            lbl = Label(self, text=name, bg='yellow')
            lbl.grid(row=emplRow, column=0, sticky='ew')

            emplPoint = []
            for col in range(len(days)):
                entryText = StringVar()
                pt = Entry(self, textvariable=entryText, width=width_entry)
                pt.grid(row=emplRow, column=col+1)
                emplPoint.append(entryText)

            self.points.append(emplPoint)
            self.savePoints.append([0 for _ in range(len(days))])



        # Save Button
        saveButton = Button(self, text="Simpan Poin")
        saveButton.grid(row=num_rows-1, column=1, columnspan=2)

        # Calculate Button
        calcButton = Button(self, text="Hitung Bonus", command=self.calculate)
        calcButton.grid(row=num_rows-1, column=3, columnspan=2)

        self.pack()
        self.center()

def main():

    root = Tk()
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()
