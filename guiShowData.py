import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
import numpy as np

#root = tk.Tk()
#root.title('F1 show stats')
#root.geometry('800x600')

#Open csv
data = pd.read_csv('driversDataFrame3.csv')

#Drop unnecesaries columns.
data = data.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])

#Take two drivers.
driver1 = data.loc[data['Nombre']=='Nico Rosberg']
driver2 = data.loc[data['Nombre']=='Keke Rosberg']

#Labels structure.
col = ('Championships', 'races', 'wins', 'pole positions', 'fastests lap', 'podiums', 'retirements', 'constructors', 'models')

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

#Show plot.
plt.show()

#root.mainloop()