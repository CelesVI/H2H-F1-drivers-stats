import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

#Create window.
root = tk.Tk()
root.title('F1 show stats')
root.geometry('800x600')

#Open csv
data = pd.read_csv('dataframe/driversDataFrame3.csv')

#Drop unnecesaries columns.
data = data.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])

#Get drivers's name.
list_drivers = data['Nombre'].tolist()

#Set list to select drivers.
combo1 = ttk.Combobox(root, value=list_drivers)
combo1.current(0)
combo1.grid(row=0,column=40, padx=2, pady=2)

combo2 = ttk.Combobox(root, value=list_drivers)
combo2.current(100)
combo2.grid(row=0,column=60, padx=2, pady=2)

def getGraph():
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
    plt.yticks(y_pos+width/2, col)
    plt.legend()

    #Adjuste view.
    plt.tight_layout()

    #Show plot.
    plt.show()

#Button to trigger graph plotting.
button = tk.Button(root, text="Compare", command=getGraph).place(x=60, y=300)

root.mainloop()