from itertools import combinations
import csv
def to_int(x):
    try: return int(x) 
    except: pass

def leerSorteos(nameFile: str):
    sorteos = []
    with open(nameFile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for line in reader:
            sorteo = list(filter(lambda x: x!=None, map(to_int, line[1:7])))
            sorteo.sort()
            sorteos.append(sorteo)
    return sorteos


def obtener_sorteos_de_cuatro(sorteos):
    sorteos4, sorteos_final = [], []
    for x in sorteos:
        sorteos4 += list(map(list, combinations(x, 4)))
    for sorteo in sorteos4:
        sorteo.sort()
        sorteos_final.append(sorteo)
    return sorteos_final
    

sorteos = leerSorteos('bonoloto.csv')
sorteos4 = obtener_sorteos_de_cuatro(sorteos)
combinaciones = list((map(list, combinations(range(1, 50), 4))))

frecuencia = {}
for id, comb in enumerate(combinaciones):
    frecuencia[id] = {'comb': comb, 'f':0, 's':sum(comb) }
    if comb in sorteos4: 
        frecuencia[id]['f'] = sorteos4.count(comb)
        
frecuencia_sort = dict(sorted(frecuencia.items(), key=lambda x: x[1]['f'], reverse=True))
for x in frecuencia_sort.items():
    print(x)
    



