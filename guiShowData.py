import matplotlib.pyplot as plt
import tkinter as tk
import pandas as pd
import numpy as np

#root = tk.Tk()
#root.title('F1 show stats')
#root.geometry('800x600')

data = pd.read_csv('driversDataFrame3.csv')
data = data.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
driver1 = data.loc[data['Nombre']=='Nico Rosberg']
driver2 = data.loc[data['Nombre']=='Keke Rosberg']

col = ('Championships', 'races', 'wins', 'pole positions', 'fastests lap', 'podiums', 'retirements', 'constructors', 'models')
y_pos = np.arange(len(col))
x_col1 = driver1.to_numpy()
x_col2 = driver2.to_numpy()
width = 0.3
new_col1 = np.delete(x_col1, 0)
new_col2 = np.delete(x_col2, 0)

#dimension_col = len(new_col1)

#line1 = plt.barh(y_pos, new_col1, height=0.3, align='center', color='purple', label=driver1['Nombre'])
#line2 = plt.barh(y_pos + width, new_col2, height=0.3, align='center', color='red', label=driver2['Nombre'])

plt.barh(y_pos, new_col1, height=0.3, align='center', color='purple', label=driver1['Nombre'].values[0])
plt.barh(y_pos + width, new_col2, height=0.3, align='center', color='red', label=driver2['Nombre'].values[0])

for i, v in enumerate(new_col1):
    plt.text(v, i, " "+str(v), color='purple', va='center')

for i, v in enumerate(new_col2):
    plt.text(v, i+width, " "+str(v), color='red', va='center')


plt.yticks(y_pos+width/2, col)
plt.legend()

plt.show()

#root.mainloop()