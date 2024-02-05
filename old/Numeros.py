from itertools import combinations
import functools
import numpy as np

def leerSorteos(nameFile: str):
    sorteosFile = open(nameFile, 'r+')    
    line :str = sorteosFile.readline()
    listaSorteos = []
    while line:
        if line != '':
            acertante = line.strip().split(',')
            sorteo = [int(s) for s in acertante[1:7] if s]
            sorteo.sort()
            listaSorteos.append([sorteo, set(sorteo)])
        line = sorteosFile.readline()
    return listaSorteos

def get_numeros_totales(sorteos, pos=-1):
    numeros_totales = []
    for item in sorteos:
        lista = item[0]
        for index, numero in enumerate(lista):
            if (index == pos) or (pos==-1):
                numeros_totales.append(numero)
    return numeros_totales

def calcular_frecuencias(numeros_totales, total_sorteos):
    frecuencia = {}
    for numero in range(1, 50):
        frecuencia[numero] = numeros_totales.count(numero) /  total_sorteos
    frecuencia = dict(sorted(frecuencia.items(), key=lambda x:x[1], reverse=False))
    return frecuencia

def not_is_cero(x):
    return x[1] > 0 

def is_cero(x):
    return x[1] == 0.0 

def obtener_frecuencias(sorteos):
    frecuencias_totales = {}
    for pos in range(0, 6):
        numeros_totales = get_numeros_totales(sorteos, pos)
        frecuencia = calcular_frecuencias(numeros_totales, len(sorteos))
        frecuencias_totales.update(dict(filter(not_is_cero, frecuencia.items())))

    return frecuencias_totales


sorteos = leerSorteos('bonoloto.csv')

test = sorteos[0:20]
train = sorteos[20:29]

while len(test) > 0:
    ganadora = test.pop()
    frecuencias = obtener_frecuencias(train)
    lista = set([x for x in frecuencias])
    combinaciones = list(combinations(list(lista), 6))

    print(len(lista), lista, ganadora[1], len(lista.intersection(ganadora[1])), 'numero combinaciones: %d' % (len(combinaciones)), sep=' - ')    
    #print('.................ACERTADAS.........................')
    #imprimirLista(acertadas, n=0)
    #print('.................ACERTADAS.........................')
    train.insert(0, ganadora)
    train = train[0:9]
    

train = train[0:9]
frecuencias = obtener_frecuencias(train)
lista = set([x for x in frecuencias])
combinaciones = list(combinations(list(lista), 6))    
print(len(lista), lista, 'numero combinaciones: %d' % (len(combinaciones)), sep=' - ')    