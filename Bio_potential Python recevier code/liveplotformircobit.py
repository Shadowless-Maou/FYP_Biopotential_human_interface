# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:25:31 2019

@author: mm
"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import serial as sr

#------global variables
data = np.array([])
cond = False

#-----plot data-----
def plot_data():
    global cond, data
    
    if (cond == True):
        
        a = s.readline()
        a.decode()
        
        if(len(data) < 100):
            data = np.append(data,float(a[0:4]))
        else:
            data[0:99] = data[1:100]
            data[99] = float(a[0:4])
		
        lines.set_xdata(np.arange(0,len(data)))
        lines.set_ydata(data)
        
        canvas.draw()
    
    root.after(1,plot_data)

def plot_start():
    global cond
    cond = True
    s.reset_input_buffer()

def plot_stop():
    global cond
    cond = False
    

#-----Main GUI code-----
root = tk.Tk()
root.title('Real Time Plot')
root.configure(background = 'light blue')
root.geometry("700x500") # set the window size

#------create Plot object on GUI----------
# add figure canvas
fig = Figure();
ax = fig.add_subplot(111)

#ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples
ax.set_title('Serial Data');
ax.set_xlabel('Sample')
ax.set_ylabel('Voltage')

ax.set_xlim(0,100)
ax.set_ylim(0,5000)
lines = ax.plot([],[])[0]

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().place(x = 10,y=10, width = 500,height = 400)
canvas.draw()

#----------create button---------
root.update();
start = tk.Button(root, text = "Start", font = ('calbiri',12),command = lambda: plot_start())
start.place(x = 100, y = 450 )

root.update();
stop = tk.Button(root, text = "Stop", font = ('calbiri',12), command = lambda:plot_stop())
stop.place(x = start.winfo_x()+start.winfo_reqwidth() + 20, y = 450)

#----start serial port----
s = sr.Serial('/dev/ttyACM0',115200);
s.reset_input_buffer()



root.after(1,plot_data)
root.mainloop()
