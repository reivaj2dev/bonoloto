from libs.utils import *
from datetime import datetime
from itertools import combinations

pd.set_option('display.max_rows', 500)
print('Iniciando: ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

dtypes={'N1':int, 'N2':int, 'N3':int, 'N4':int, 'N5':int, 'N6':int, 
        'aciertos_0':int, 'aciertos_1':int, 'aciertos_2':int, 'aciertos_3':int, 
        'aciertos_4':int, 'aciertos_5':int, 'aciertos_6':int}

sorteos, name_files = [], ['data/bonoloto.csv', 'data/bonoloto2.csv']
for name_file in name_files:
        sorteos += leer_sorteos(name_file)
sorteos.sort(key=lambda x:x[0])        

n = len(sorteos)-100
train = sorteos[2000:n]
test = sorteos[n:]
print(train[-1])
print(test[0])
test = sorteos[n:]

##########################
def filtrar(frios, listas, item):
        item_to_list = list(item)
        for l in listas:
                if (len(set(item_to_list).intersection(l)) > 2 or len(set(item_to_list).intersection(frios)) > 3):
                        return False
        return True

def obtener_seleccionadas(combinaciones, *argv):
        frios, listas = argv
        seleccionadas = list(filter(lambda item: filtrar(frios, listas, item), combinaciones))
        return seleccionadas[0:10]

combinaciones = combinations(range(1, 50), 6)
while len(test) > 0:
        sorteos_df = pd.DataFrame(train, columns=['FECHA', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6'])
        ganadora = test.pop(0)
        freq = obtener_frecuencias(train, n=0, fecha=train[-1][0])
        freq['DIFF'] = freq['ULTIMA_VEZ'] - freq['MEDIA_DIAS']
        freq.sort_values(by=['DIFF'], ascending=False, inplace=True)
        
        listas = []
        for i in range(0, 10):
                freq_item = freq[(freq.ULTIMA_VEZ == i)].copy()
                freq_item.sort_values(by=['FREQ'], ascending=False, inplace=True)
                listas.append(freq_item.N.to_list())
        freq_item = freq[(freq.ULTIMA_VEZ >= 10)].copy()
        freq_item.sort_values(by=['FREQ'], ascending=False, inplace=True)
        frios = freq_item.N.to_list()
        set_ganadora = set(ganadora[1:])
        seleccionadas = obtener_seleccionadas(combinaciones, frios, listas)
        print(len(seleccionadas))

        #Añadimos la fila del sorteocelebrado al final
        train.append(ganadora)
        input('...')
        
        

'''
sorteos_df = pd.DataFrame(sorteos, columns=['FECHA', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6'])
sorteos_df = obtener_probs_numeros(sorteos_df, freq)
sorteos_df, suma_df, resta_df, d1_df, d2_df, d3_df, d4_df, d5_df, pares_df = generar_estadisticas(sorteos_df)
sorteos_df['PROB1'] = sorteos_df[['P1', 'P2', 'P3', 'P4', 'P5', 'P6']].product(axis=1)
sorteos_df['PROB2'] = sorteos_df[['P_SUMA', 'P_RESTA', 'P_NUM_PARES', 'P_D1', 'P_D2', 'P_D3', 'P_D4', 'P_D5']].product(axis=1)
sorteos_df['PROB'] = sorteos_df[['PROB1', 'PROB2']].product(axis=1)
sorteos_df = sorteos_df[sorteos_df.PROB > 0].copy()
media = sorteos_df['PROB'].
mean()
moda = sorteos_df['PROB'].mode()
moda1= moda[0]
probabilidades = {'SUMA':suma_df, 'RESTA':resta_df, 'D1':d1_df, 'D2':d2_df, 'D3':d3_df, 'D4':d4_df, 'D5':d5_df , 'NUM_PARES': pares_df }
#check_metodo(sorteos)

print(pares_df)
print(suma_df)
print(resta_df)

combinaciones = obtener_combinaciones(range(1, 50))
combinaciones = obtener_probs_numeros(combinaciones, freq)
combinaciones = combinaciones[(combinaciones.N1.isin([1,2,3,4,5,6]))
        & (combinaciones.N2.isin([9,10,15,7,13,14,5,16,17,20]))
        & (combinaciones.N3.isin([13,23,27,30,16,20,21,24,31,15,17,26,28]))
        & (combinaciones.N4.isin([31,39,26,32,36,34,21,27,35,40,23,28]))
        & (combinaciones.N5.isin([41,42,39,40,37,43,44,33,46,30]))
        & (combinaciones.N6.isin([49,48,46,45,47]))].copy()
combinaciones = genera_valores(combinaciones)
combinaciones['ORDEN'] = (combinaciones['NUM_PARES']-3).abs()
combinaciones.sort_values(by=['ORDEN'], ascending=True, inplace=True)
combinaciones = combinaciones[(combinaciones.NUM_PARES.isin([2,3,4]))].copy()
combinaciones.reset_index(drop=True, inplace=True)
combinaciones = obtener_aciertos(sorteos_df, combinaciones)
print(combinaciones)
'''
