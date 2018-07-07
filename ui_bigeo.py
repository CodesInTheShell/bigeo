import bigeo
from tkinter import *
from tkinter import messagebox, ttk

class MainGUI:

    def __init__(self, master):

        master.title("Bigeo - Automated geospatial processing software")
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.geometry("1010x600+20+20") #1210

# --------------------------- MENU --------------------------------------

        mainMenu = Menu(master)
        master.config(menu=mainMenu)
        fileMenu = Menu(mainMenu)
        mainMenu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=self.eventTester)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=master.destroy)

        aboutMenu = Menu(mainMenu)
        mainMenu.add_cascade(label="About", menu=aboutMenu)
        aboutMenu.add_command(label="About this software", command=self.eventAbout)

        helpMenu = Menu(mainMenu)
        mainMenu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="How to", command=self.eventHelp)


# ----------------------------- FRAMES ---------------------------------

        logoFrame = Frame(master, bd=8, relief="raised")
        logoFrame.grid(row=0, column=0, sticky=N+E+W+S)

        setupFrame = Frame(master, bd=8, relief="raised", pady=5)
        setupFrame.grid(row=1, column=0, sticky=N+E+W+S)

        frameResult = Frame(master, bd=8, relief="raised")
        frameResult.grid(row=2, column=0, sticky=N+W+E+S)

        statusFrame = Frame(master, bd=8, relief="raised")
        statusFrame.grid(row=3, column=0, sticky=N+W+E+S)

# ------------------------- LOGO HEADER --------------------------------

        iconLabel = Label(logoFrame, text="B", bg="red", font=('arial', 50, 'bold'))
        iconLabel.grid(row=0, column=0)
        logoLabel = Label(logoFrame, text="Bigeo - Automated geospatial processing software", bg="yellow", font=('arial', 20, 'bold'), pady=24)
        logoLabel.grid(row=0, column=1)

# ---------------------------- RESULTS FRAME ------------------------------------

        frameResultTop = Frame(frameResult, bd=8, relief="raised")
        frameResultTop.grid(row=0, column=0, columnspan=2, sticky=N + W + E)

        frameResultSelection = Frame(frameResult, bd=8, relief="raised")

        frameResultSelection.grid(row=1, column=0, columnspan=2, sticky=N + W + E)
        frameResultOutput = Frame(frameResult, bd=8, relief="raised", width=40, height=200)
        frameResultOutput.grid(row=2, column=0, sticky=N + E + S+W)


# ------------------------- LOG RESULTS WIDGETS------------------------------
        labelFeednameResults = Label(frameResultTop, text="Results",
                                          font=('helvetica', 15, 'bold'))
        labelFeednameResults.grid(row=0, column=0)

        labelSelect = Label(frameResultSelection, text="Select:            ", font=('helvetica', 12, 'bold'))
        labelSelect.grid(row=0, column=0, sticky=N + W + E)

        self.textOutput = Text(frameResultOutput, wrap=NONE)
        self.textOutput.grid(row=0, column=0, sticky=N+S+E+W)

        self.yscrollbarResult = Scrollbar(frameResult, cursor="arrow", width=20,
                                          command=self.textOutput.yview)
        self.yscrollbarResult.grid(row=2, column=1, sticky=N + S)
        self.xscrollbarResult = Scrollbar(frameResult, cursor="arrow", width=20,
                                          command=self.textOutput.xview,
                                          orient=HORIZONTAL)
        self.xscrollbarResult.grid(row=3, column=0, columnspan=2, sticky=E + W)

        self.textOutput.configure(yscrollcommand=self.yscrollbarResult.set)
        self.textOutput.configure(xscrollcommand=self.xscrollbarResult.set)

# ------------------------ EVENTS HANDLERS ------------------------------
    def eventTester(self):
        messagebox.showinfo('Title', 'It Works')

    def eventAbout(self):
        messagebox.showinfo('About', """ An automated geospatial processing software comes with algorithms and other features.
            """)

    def eventHelp(self):
        messagebox.showinfo('Help', """ For support, questions, bugs and feature request. Email at xhtrae@gmail.com """)


# ------------ START GUI --------------
root = Tk()
gui = MainGUI(root)
root.mainloop()