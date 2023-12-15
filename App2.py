from itertools import combinations
import numpy as np

def leerSorteos(nameFile: str):
    sorteosFile = open(nameFile, 'r+')    
    line :str = sorteosFile.readline()
    listaSorteos = []
    lista = []
    while line:
        line = sorteosFile.readline()
        if line != '':
            acertante = line.strip().split(',')
            sorteos = [int(s) for s in acertante[1:7] if s]
            listaSorteos.append(sorteos)
    for sorteo in listaSorteos:
        if sorteo:
            sorteo.sort()
            lista.append(sorteo)
    return lista

def comprobar(c1, c2):
    return len(set(c1).intersection(set(c2)))

def imprimirProbabilidades(probabilidades):
    for prob in probabilidades:
        print(prob)

def separarLista(listap):
    listaNumeros = []
    listaProbabilidades = []
    for elemento in listap:
        l = []
        p = []
        for n in elemento:
            l.append(n[0])
            p.append(n[1])
        listaNumeros.append(l)
        listaProbabilidades.append(p)
    return listaNumeros, listaProbabilidades

def separarLista2(listap):
    listaNumeros = []
    listaProbabilidades = []
    for elemento in listap:
        listaNumeros.append(elemento[0])
        listaProbabilidades.append(elemento[1])
    return listaNumeros, listaProbabilidades

def generarEstadistica(listaSorteos, numeros):
    posiciones = []
    for pos in range (0, 6):
        posiciones.append([sorteo[pos] for sorteo in listaSorteos])
    size = len(listaSorteos)
    listap = []
    for lista in posiciones:
        probabilidades = []
        for n in numeros:       
            apariciones = lista.count(n)
            probabilidades.append([n, round((apariciones/size),2)])    
        probabilidades.sort(key = lambda x: x[1], reverse=True)
        listap.append([prob for prob in probabilidades if prob[1] > 0])
    listaNumeros, listaProbabilidades = separarLista(listap)
    return listaNumeros, listaProbabilidades

def obtener_probabilidades_combinaciones(combinaciones, probabilidades, listaNumeros):
    listaCombinaciones = []
    for comb in combinaciones:
        probabilidad = 1
        for idx, n in enumerate(comb):
            if n in listaNumeros[idx]:
                probabilidad *= probabilidades[idx][listaNumeros[idx].index(n)]
            else:
                probabilidad *=0
        comb.append(probabilidad)
        listaCombinaciones.append(comb)
    return listaCombinaciones

def probCero(n, combinacion):
    return combinacion[n] != 0

def filtrar(sorteo, comb):
    return comprobar(comb[0:6], sorteo) < 5

def eliminarAgraciadas(listaSorteos, combinaciones):
    filtrado = []
    index, size = 0, len(listaSorteos)
    while index < size:
        sorteo = listaSorteos[index]
        combinaciones = list(filter(lambda x : filtrar(sorteo, x), combinaciones))
        index += 1
    return combinaciones

def imprimirLista(combinaciones, n=20):
    if n == 0: n=len(combinaciones) 
    for comb in combinaciones[0:n]:
        print(comb)

def calcularProbSumas(listaSumas, listaProbabilidadesSumas, comb):
    suma = sum(comb[0:6])
    prob = 0
    if suma in listaSumas:
        indice = listaSumas.index(suma)
        prob = listaProbabilidadesSumas[indice]
    comb.append(prob)
    comb.append(prob*comb[-2])
    return comb
    
def obtener_probabilidades_combinaciones(combinaciones, probabilidades, listaNumeros):
    listaCombinaciones = []
    for comb in combinaciones:
        probabilidad = 1
        for idx, n in enumerate(comb):
            if n in listaNumeros[idx]:
                probabilidad *= probabilidades[idx][listaNumeros[idx].index(n)]
            else:
                probabilidad *=0
        comb.append(probabilidad)
        listaCombinaciones.append(comb)
    return listaCombinaciones

def sumaNumeros(listaSorteos):
    sumas = [sum(sorteo) for sorteo in listaSorteos ]
    sumasUnicas = []
    for s in sumas:
        if not s in sumasUnicas:
            sumasUnicas.append(s)
    listasSumas=[]
    for s in sumasUnicas:
        listasSumas.append([s, sumas.count(s)/len(listaSorteos)])
    listasSumas.sort(key=lambda x : x[1], reverse=True)
    listaSumas, listaProbabilidades = separarLista2(listasSumas)
    return listaSumas, listaProbabilidades

def probParejas(listaSorteos, numeros, n):
    combo2 = list(combinations(numeros, n))
    comb2_list = [list(comb) for comb in combo2]
    parejas = []
    for  c2 in comb2_list:
        cj = set(c2)
        aciertos = 0
        for s in listaSorteos:
            cjs = set(s)
            if len(cjs.intersection(cj)) == len(cj):
                aciertos+=1
        c2.append(aciertos/len(listaSorteos))
        print(c2)
        parejas.append(c2)
    return parejas

def probParejas2(listaSorteos, numeros, n):
    combo2 = list(combinations(numeros, n))
    comb2_list = [list(comb) for comb in combo2]
    parejas = []
    l = []
    total = []
    for c2 in comb2_list:
        cj = set(c2)
        aciertos = 0
        for s in listaSorteos:
            cjs = set(s)
            if len(cjs.intersection(cj)) == len(cj):
                aciertos+=1
        c2.append(aciertos/len(listaSorteos))
        if not aciertos in l:
            l.append(aciertos)
        total.append(aciertos)
        parejas.append(c2)
    for i in l:
        print(i, total.count(i))
    input('....')
    return parejas

def obtener_prob(comb, x):
    setC = set(comb[0:6])
    setP = set(x[0:-1])
    if len(setC.intersection(setP)) == len(setP):
        return x[-1]
    return 1
    
def calcularProbParejas(probabilidades, comb):
    prob = np.prod(list(map(lambda x : obtener_prob(comb[0:6], x), probabilidades)))
    if (prob == 1): prob = 0     
    comb.append(prob)
    comb.append(prob*comb[-2])
    return comb

#Esto esta correcto
presupuesto = 10
precioApuesta = 0.5
apuestasTotales = 10/precioApuesta
print('%d apuestas a imprimir' % (int(apuestasTotales)))
numeros :list = [n for n in range(1, 50)]

listaSorteos = leerSorteos('bonoloto.csv') 
listaSorteos2 = leerSorteos('bonoloto2.csv')
listaSorteos = listaSorteos+listaSorteos2
print('Cargados %d sorteos' %(len(listaSorteos)))
combinaciones = list(combinations(numeros, 6))
combinaciones = [list(comb) for comb in combinaciones]
print('%d combinaciones' %(len(combinaciones)))

filtradas = eliminarAgraciadas(listaSorteos, combinaciones)
print('%d combinaciones' %(len(filtradas)))

file = open('combinaciones.csv', 'a+')
for comb in filtradas:
    file.write(",".join([str(x) for x in comb])+'\n')
file.close()

'''
listaSumas, listaProbabilidades = sumaNumeros(listaSorteos)
listaNumeros, probabilidades = generarEstadistica(listaSorteos, numeros)
print('Probabilidades de numeros calculadas')
probCombinaciones = obtener_probabilidades_combinaciones(combinaciones, probabilidades, listaNumeros)
print('Probabilidad de combinaciones calculadas')
probCombinacionesfilter = list(filter(lambda x: probCero(6, x), probCombinaciones))
print('%d combinaciones' %(len(probCombinacionesfilter)))

probCombinacionesfilter = list(map(lambda x: calcularProbSumas(listaSumas, listaProbabilidades, x),  probCombinacionesfilter))
probCombinacionesfilter = list(filter(lambda x: probCero(8, x), probCombinacionesfilter))
print('%d combinaciones 1' %(len(probCombinacionesfilter)))

#Tarda bastante como medio dia

probCombinacionesfilter = list(filter(lambda x: x[0] == 1,  probCombinacionesfilter))
print('filtrando %d combinaciones 1.5' %(len(probCombinacionesfilter)))

prob = probParejas(listaSorteos, numeros, 2)
probCombinacionesfilter = list(map(lambda x: calcularProbParejas(prob, x),  probCombinacionesfilter))
print('filtrando %d combinaciones 2' %(len(probCombinacionesfilter)))
probCombinacionesfilter = list(filter(lambda x: probCero(10, x), probCombinacionesfilter))
print('%d combinaciones 2' %(len(probCombinacionesfilter)))

prob = probParejas(listaSorteos, numeros, 3)
probCombinacionesfilter = list(map(lambda x: calcularProbParejas(prob, x),  probCombinacionesfilter))
print('filtrando %d combinaciones 3' %(len(probCombinacionesfilter)))
probCombinacionesfilter = list(filter(lambda x: probCero(12, x), probCombinacionesfilter))
print('ordenando %d combinaciones 3' %(len(probCombinacionesfilter)))
probCombinacionesfilter.sort(key=lambda x: x[12], reverse=True)
print('%d combinaciones 3' %(len(probCombinacionesfilter)))
imprimirLista(probCombinacionesfilter, 10)


#Tarda bastante como medio dia
#filtradas = eliminarAgraciadas(listaSorteos, probCombinacionesfilter)
#print('%d combinaciones' %(len(filtradas)))
#imprimirLista(filtradas)
'''