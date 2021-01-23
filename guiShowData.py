import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

#Create window.
root = tk.Tk()
root.title('F1 show stats')
root.geometry('800x600')

#Add image background.
backgroud_image = tk.PhotoImage(file='background/f1logo.png')
backgroud_label = tk.Label(root, image=backgroud_image)
backgroud_label.place(relwidth=1, relheight=1)

#Testing global canvas.
canvas = None
toolbar = None

#Open csv
data = pd.read_csv('dataframe/driversDataFrame3.csv')

#Drop unnecesaries columns.
data = data.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])

#Get drivers's name.
list_drivers = data['Nombre'].tolist()

#Add lables.
label1 = tk.Label(root, text="Driver 1").place(x=275, y=0)
label2 = tk.Label(root, text="Driver 2").place(x=275, y=20)

#Set list to select drivers.
combo1 = ttk.Combobox(root, value=list_drivers)
combo1.current(0)
combo1.place()
combo1.pack()

combo2 = ttk.Combobox(root, value=list_drivers)
combo2.current(1)
combo2.place()
combo2.pack()

def clearGraph():
    #Destroy previous graph
    canvas.get_tk_widget().pack_forget()
    toolbar.destroy()

def getGraph():
    #Call the global variable.
    global canvas
    global toolbar

    #Destroy previous graph
    if canvas != None and toolbar != None:
        canvas.get_tk_widget().pack_forget()
        toolbar.destroy()

    #Create Figure and subplot.
    fig = Figure(figsize=(6,5), dpi=80)
    plt = fig.add_subplot(111)
    
    #Take the selected drivers.
    name1 = combo1.get()
    name2 = combo2.get()

    #Get drivers data.
    driver1 = data.loc[data['Nombre']== name1]
    driver2 = data.loc[data['Nombre']== name2]

    #Labels structure.
    col = ('Championships', 'Races', 'Wins', 'Pole positions', 'Fastests lap', 'Podiums', 'Retirements', 'Constructors', 'Models')

    #Calculate col array lenght to match labels to graph later.
    y_pos = np.arange(len(col))

    #Convert driver dataframe row into numpy array.
    x_col1 = driver1.to_numpy()
    x_col2 = driver2.to_numpy()
    width = 0.3

    #Delete driver namer form array.
    new_col1 = np.delete(x_col1, 0)
    new_col2 = np.delete(x_col2, 0)

    #Create barh plots.
    plt.barh(y_pos, new_col1, height=0.3, align='center', color='purple', label=driver1['Nombre'].values[0])
    plt.barh(y_pos + width, new_col2, height=0.3, align='center', color='red', label=driver2['Nombre'].values[0])

    #Add label right to bars.
    for i, v in enumerate(new_col1):
        plt.text(v, i, " "+str(v), color='purple', va='center')

    for i, v in enumerate(new_col2):
        plt.text(v, i+width, " "+str(v), color='red', va='center')

    #Positionate labels.
    plt.set_yticks(y_pos+width/2)
    plt.set_yticklabels((col))
    plt.legend()

    #Create a canvas to draw the plot.
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw() 
  
    #Place the canvas on the Tkinter window 
    canvas.get_tk_widget().pack(fill=tk.BOTH, side=tk.BOTTOM) 
  
    #Create the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, root) 
    toolbar.update() 
  
    #Place the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack() 
    
    #Adjuste view.
    #plt.tight_layout()

    #Show plot.
    #plt.show() 

#Button to trigger graph plotting.
button1 = tk.Button(master=root, text="Compare", command=getGraph).place(x=300, y=100)
button2 = tk.Button(master=root, text="Clear", command=clearGraph).place(x=400, y=100)

root.mainloop()