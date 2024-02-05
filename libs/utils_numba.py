import csv
from datetime import datetime
from statistics import median
import numpy as np
from itertools import combinations
from numba import jit
n=49
__numeros = np.arange(1, 50)

jit(nopython=True)
def to_int(x):
    try: return int(x) 
    except: pass

jit(nopython=True)
def leer_sorteos(nameFile: str):
    sorteos = []
    with open(nameFile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for line in reader:
            try:
                fecha = datetime.strptime(line[0], '%d/%m/%Y').date()
                sorteo = list(filter(lambda x: x!=None, map(to_int, line[1:7])))
                sorteo.sort()
                sorteos.append([fecha]+sorteo)
            except:
                pass            
    return sorteos


jit(nopython=True)
def obtener_combinaciones():
    combinaciones = np.matrix(list(combinations(__numeros, 6)))

    suma = combinaciones[:, 0:6].sum(axis=1)
    suma_col = suma.reshape(-1, 1)
    combinaciones = np.hstack((combinaciones, suma_col))

    resta = combinaciones[:, 5] - combinaciones[:, 4] - combinaciones[:, 3] - combinaciones[:, 2] - combinaciones[:, 1] - combinaciones[:, 0]
    resta_col = resta.reshape(-1, 1)
    combinaciones = np.hstack((combinaciones, resta_col))

    for i in range(1, 6):
        opreracion = combinaciones[:, i] - combinaciones[:, (i-1)]
        opreracion_col = opreracion.reshape(-1, 1)
        combinaciones = np.hstack((combinaciones, opreracion_col))

    return combinaciones

print(obtener_combinaciones())
sorteos, name_files = [], ['data/bonoloto.csv', 'data/bonoloto2.csv']
for name_file in name_files:
    sorteos += leer_sorteos(name_file)
sorteos = np.matrix(sorteos)
print(sorteos)