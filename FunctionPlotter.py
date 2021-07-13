from PySide2.QtGui import QFont
from PySide2.QtWidgets import QApplication, QGridLayout, QGroupBox, QLabel, QMainWindow, QPushButton, QTextEdit, QVBoxLayout,QWidget
from PySide2.QtCore import Qt

import math

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#Setting correct backend for matplotlib
matplotlib.use('Qt5Agg')
matplotlib.rc('xtick',labelsize=10)
matplotlib.rc('ytick',labelsize=10)

#To safely execute eval() function later
eval_params = {'__builtins__':None,'e':math.e,'sin':math.sin,'cos':math.cos,'tan':math.tan}

import sys

#Defining the main window
class Window(QMainWindow):
    def __init__(self):
        #Inheriting main class attributes
        super().__init__()
        #Setting start_position, width, height and title
        width = 800
        height = 600
        self.setWindowTitle("Function Plotter")
        self.setGeometry(300,100,width,height)

        #Creating Grid layout and returning references to I/O widgets
        self.pltbtn,self.xmin_box,self.xmax_box,self.eqn_box,self.info_box,self.plt,self.fig =  self.createGridLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

    def createGridLayout(self,prev_log = ('',)*4,ax = None,fig=None):
        self.groupBox = QGroupBox("Plotting parameters:")
        self.groupBox.setFont(QFont('Sanserif',11))
        gridLayout = QGridLayout()

        #Creating labels, textBoxes and buttons, and adding them to our grid

        x_min_label = QLabel("x min:",self)
        x_min_label.setFont(QFont('Sanserif',9))
        gridLayout.addWidget(x_min_label,0,0)

        x_max_label = QLabel("x max:",self)
        x_max_label.setFont(QFont('Sanserif',9))
        gridLayout.addWidget(x_max_label,2,0)

        eqn_label = QLabel("f(x):",self)
        eqn_label.setFont(QFont('Sanserif',9))
        gridLayout.addWidget(eqn_label,4,0)

        xmintxtbox = QTextEdit("",self)
        xmintxtbox.setMaximumHeight(29)
        gridLayout.addWidget(xmintxtbox,1,0)
        xmintxtbox.setText(prev_log[0])

        xmaxtxtbox = QTextEdit("",self)
        xmaxtxtbox.setMaximumHeight(29)
        gridLayout.addWidget(xmaxtxtbox,3,0)
        xmaxtxtbox.setText(prev_log[1])

        eqntxtbox = QTextEdit("",self)
        eqntxtbox.setMaximumHeight(29)
        gridLayout.addWidget(eqntxtbox,5,0)
        eqntxtbox.setText(prev_log[2])

        pltbtn = QPushButton("Plot",self)
        pltbtn.setFont(QFont('Sanserif',9))
        pltbtn.clicked.connect(self.plot)
        gridLayout.addWidget(pltbtn,6,0)

        infotxtbox = QTextEdit("Logs:",self)
        infotxtbox.setFont(QFont('Sanserif'))
        infotxtbox.setReadOnly(True)
        infotxtbox.setTextColor(Qt.red)
        infotxtbox.setText(prev_log[3])
        gridLayout.addWidget(infotxtbox,0,1,7,1)

        #Creating matplotlib figure
        if ax is None or fig is None:
            fig = Figure(dpi=75)
            ax = fig.add_subplot(111)
        
        #Creating a canvas and adding it as a widget to our main Grid Layout
        canvas = FigureCanvas(fig)
        gridLayout.addWidget(canvas,7,0,1,2)
        

        self.groupBox.setLayout(gridLayout)

        return pltbtn,xmintxtbox,xmaxtxtbox,eqntxtbox,infotxtbox,ax,fig
        
    def plot(self):
        #Reseting plot
        self.fig = Figure(dpi=75)
        self.plt = self.fig.add_subplot(111)
        self.info_box.setText("Logs:")
        err_msg = ""
        gt = True
        #Reading inputs and validating them
        try:
            x_min = float(self.xmin_box.toPlainText())
        except:
            err_msg+="\nInvalid value for x_min!"
        try:
            x_max = float(self.xmax_box.toPlainText())
            gt = x_max > x_min
            assert(gt)
        except:
            err_msg+="\nInvalid value for x_max!"
            if not gt:
                err_msg+="\nMax value cannot exceed Min value!"
        try:
            eqn = self.eqn_box.toPlainText()
            #Ensuring eqn is ready for eval function
            eqn = eqn.replace('^','**')
            assert(eqn!="")
            assert(eqn.count('&')==0)
            assert(eqn.count('or')==0)
            assert(eqn.count('and')==0)
            assert(eqn.count('|')==0)
            assert(eqn.count('!')==0)
            assert(eqn.count('<')==0)
            assert(eqn.count('>')==0)
            x = 1
            #Validating f(x) by evaluating it on arbitrary value of x (let x=1)
            eval(eqn,eval_params,{'x':x})
        except:
            err_msg+="\nInvalid function!"
        if len(err_msg)>0:
            self.info_box.setText('Error!'+err_msg)
            return
        x = x_min
        fail = False
        while(x<x_max-0.1):
            try:
                f = eval(eqn,eval_params,{'x':x})
                x+=0.1
                f_df = eval(eqn,eval_params,{'x':x})

                #Adding a small line (x,f) -> (x+dx ,f + df)
                self.plt.plot([x-0.1,x],[f,f_df],"-b")
            except:
                #Exception due too overflow
                fail = True
                break
        if(fail):
            self.info_box.setText("Log:\n"+"A number may have exceeded the maximum of matplotlib")
        else:
            self.info_box.setText("Log:\n"+"Plotting is successful!")

        #Resetting layout and drawing everything again   
        self.hide()
        prev_log = (self.xmin_box.toPlainText(),self.xmax_box.toPlainText(),self.eqn_box.toPlainText(),self.info_box.toPlainText())
        self.pltbtn,self.xmin_box,self.xmax_box,self.eqn_box,self.info_box,self.plt,self.fig =  self.createGridLayout(prev_log,self.plt,self.fig)
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.show()
        
if(__name__ == "main"):
    #Inistantiating app and Window
    app = QApplication([])
    window = Window()
    #Showing window and calling a thread
    window.show()
    app.exec_()  