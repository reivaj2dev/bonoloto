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

def imprimirLista(combinaciones, n=20):
    if n == 0: n=len(combinaciones) 
    for comb in combinaciones[0:n]:
        print(comb)

def not_empty(x):
    return len(set(x[0])) > 0

def not_is_cero(x):
    return x[7] > 0

def is_cero(x):
    return x[7] == 0

def suma(sorteo):
    sorteo.append(functools.reduce(lambda x, y: x+y, sorteo[0]))
    return sorteo

def resta(sorteo):
    sorteo.append(functools.reduce(lambda x, y: x-y, sorteo[0]))
    return sorteo

def probabilidades_digitos(listaSorteos):
    posiciones = [[] for _ in tuple(listaSorteos[0][0])]
    grupos = [[] for _ in tuple(listaSorteos[0][0])]
    probabilidades = [[] for _ in tuple(listaSorteos[0][0])]
    for sorteo in listaSorteos: 
        combinacion = sorteo[0]
        for pos, numero in enumerate(combinacion):
            posiciones[pos].append(numero)
            if not numero in grupos[pos]:
                grupos[pos].append(numero)
    for pos, grupo in enumerate(grupos):
        for numero in grupo:
            probabilidades[pos].append([numero, posiciones[pos].count(numero)/len(listaSorteos)])
    return grupos, probabilidades

def probabilidades_posiciones(posiciones, probabilidad_digitos, combinacion):
    comb = combinacion[0]
    prob = 1
    for pos, numero in enumerate(comb):
        if numero in posiciones[pos]:
            indice =  posiciones[pos].index(numero)
            prob *= probabilidad_digitos[pos][indice][1]
    combinacion.append(prob)
    return combinacion

def filtrar_posiciones(posiciones, combinacion):
    comb = combinacion[0]
    for pos, numero in enumerate(comb):
        if numero in posiciones[pos]:
            return True
    return False

def probabilidades_operaciones(listaSorteos, index):
    sumas = [sorteo[index] for sorteo in listaSorteos]
    grupos = []
    for num in sumas:
        if not num in grupos:
            grupos.append(num)
    lista_op_numeros = [numero for numero in sumas]
    probsDigitos = [sumas.count(numero)/len(sumas) for numero in sumas]
    return lista_op_numeros, probsDigitos

def search_op(numero, x):
    return x[0] == numero

def calcular_probabilidades(op, lista_op_numeros, probabilidades, combinacion):
    suma = combinacion[op]
    if suma in lista_op_numeros:
        indice = lista_op_numeros.index(suma)
        combinacion.append(probabilidades[indice])
    else:
        combinacion.append(0)
    return combinacion

def calcular_probabilidad_total(combinacion):
    probabilidad = functools.reduce(lambda x, y: x*y, combinacion[4:])
    combinacion.append(probabilidad)
    return combinacion

def obtener_numeros(sorteos):
    numeros = []
    for sorteo in sorteos:
        conjunto = sorteo[0]
        for digito in conjunto:
            numeros.append(digito)
    return list(set(numeros))

def genera_combinaciones(numeros, listaSorteos, ganadora):
    op_suma, op_resta = 2, 3
    posiciones, probabilidad_digitos = probabilidades_digitos(listaSorteos)
    sumas, probabilidad_sumas = probabilidades_operaciones(listaSorteos, op_suma)
    restas, probabilidad_resta = probabilidades_operaciones(listaSorteos, op_resta)

    combinaciones = list(map(lambda comb: [list(comb), set(comb)], combinations(numeros, 6)))
    print('%d combinaciones 0' %(len(combinaciones)))

    combinaciones = list(map(suma, combinaciones))
    combinaciones = list(map(resta, combinaciones))

    print('%d combinaciones 1' %(len(combinaciones)))
    combinaciones = list(filter(lambda combinacion: filtrar_posiciones(posiciones, combinacion), combinaciones))

    print('%d combinaciones 2' %(len(combinaciones)))
    combinaciones = list(map(lambda combinacion: probabilidades_posiciones(posiciones, probabilidad_digitos, combinacion), combinaciones))

    combinaciones = list(map(lambda combinacion: calcular_probabilidades(op_suma, sumas, probabilidad_sumas, combinacion), combinaciones))
    print('%d combinaciones 3' %(len(combinaciones)))

    combinaciones = list(map(lambda combinacion: calcular_probabilidades(op_resta, restas, probabilidad_resta, combinacion), combinaciones))
    print('%d combinaciones 4' %(len(combinaciones)))
    combinaciones = list(map(calcular_probabilidad_total, combinaciones))
    combinaciones = list(filter(not_is_cero, combinaciones))
    combinaciones.sort(key=lambda x: x[7], reverse=True)

    '''
        Estamos en este punto se elimnan unas 136732 combinaciones
        una mierda pinchada en un palo.
    '''

    print('%d combinaciones 6' %(len(combinaciones)))
    return combinaciones

def check(ganadora, combinacion):
    return len(ganadora[1].intersection(combinacion[1])) >= 3

def check_add(ganadora, combinacion):
    combinacion.append(len(ganadora[1].intersection(combinacion[1])))
    return combinacion

def reduccion(combinaciones):
    lista = []
    first = combinaciones.pop(0)
    lista.append(first)
    while (len(combinaciones) > 0) or len(lista) == 50:
        siguiente = combinaciones.pop(0)
        if (len(first[1].intersection(siguiente[1])) == 0):
            lista.append(siguiente)
    return lista

presupuesto = 10
precioApuesta = 0.5
apuestasTotales = 10/precioApuesta
print('%d apuestas a imprimir' % (int(apuestasTotales)))
numeros :list = [n for n in range(1, 50)]
listaSorteos = leerSorteos('bonoloto.csv')
listaSorteos = list(filter(not_empty, listaSorteos))
listaSorteos = list(map(suma, listaSorteos))
listaSorteos = list(map(resta, listaSorteos))

op_suma, op_resta = 1, 2
posiciones, probabilidad_digitos = probabilidades_digitos(listaSorteos)
sumas, probabilidad_sumas = probabilidades_operaciones(listaSorteos, op_suma)
restas, probabilidad_resta = probabilidades_operaciones(listaSorteos, op_resta)

test = listaSorteos[0:20]
train = listaSorteos[20:27]
print(len(test), len(train))
while len(test) > 0:
    ganadora = test.pop()
    print('ganadora: ', ganadora)
    numeros = range(1, 50)#obtener_numeros(train)
    
    print('numeros: ', numeros, 'Numeros Totales: ', len(numeros), 'Incluidos:', len(set(numeros).intersection(ganadora[0])) )
    combinaciones = genera_combinaciones(numeros, listaSorteos, ganadora)
    
    #print('Aplicando reduccion...')
    #combinaciones = reduccion(combinaciones)
    #combinaciones = combinaciones[0:50]
    #lista_set = [x[1] for x in combinaciones]    
    #combinaciones = list(map(lambda x: check_add(ganadora, x), combinaciones))
    #imprimirLista(combinaciones, n=50)
    #acertadas = list(filter(lambda x: check(ganadora, x), combinaciones))
    #print('.................ACERTADAS.........................')
    #imprimirLista(acertadas, n=0)
    train.insert(0, ganadora)
    train = train[0:7]
    #print('.................ACERTADAS.........................')
    input('....')
