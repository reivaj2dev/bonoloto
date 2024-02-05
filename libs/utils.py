import csv
from datetime import datetime
from statistics import median
import pandas as pd
from itertools import combinations
import sys

def get_date():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
n=49
__numeros = list(range(1, (n+1)))

def print_secuencia(texto, secuencia, final=0):
    if final == 0:
        sys.stdout.write(f"\r{texto}: {secuencia}")
    else:
        sys.stdout.write(f"\r{texto}: {secuencia} de {final}")
    sys.stdout.flush()    

def to_int(x):
    try: return int(x) 
    except: pass

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

def obtener_dias(numero, sorteos, current_date=None):
    sorteos.sort(key=lambda x:x[0], reverse=True)        
    current_date = datetime.now().date() if not current_date else current_date
    pasados, fecha_inicial, dias = None, None, []
    for sorteo in sorteos:
        sorteo_num = sorteo[1:]
        if numero in sorteo_num:
            if not fecha_inicial:
                fecha_inicial = sorteo[0]
                pasados = (current_date-fecha_inicial).days
            else:
                dias.append((fecha_inicial-sorteo[0]).days)
                fecha_inicial = sorteo[0]
    sorteos.sort(key=lambda x:x[0], reverse=False)                        
    return median(dias), pasados

def numeros_x_pos(sorteos):
    lista_numeros = [[], [], [], [], [], []]
    for sorteo in sorteos:
        for pos, n in enumerate(sorteo[1:]):
            lista_numeros[pos].append(n)
    return lista_numeros

def obtener_frecuencias(sorteos, n=0, fecha= None):
    n = len(sorteos) if n == 0 else n
    df = pd.DataFrame([], columns=['N', 'PROB', 'FREQ', 'MEDIA_DIAS', 'ULTIMA_VEZ', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6'])
    lista_numeros = [n for sorteo in sorteos[0:n] for n in sorteo[1:]]
    numeros_in_pos = numeros_x_pos(sorteos[0:n])
    for numero in __numeros:
        lista = []
        count = lista_numeros.count(numero)
        probabilidad = round(count / len(sorteos), 4)
        dias, pasados = obtener_dias(numero, sorteos, fecha)        
        lista.append([numero, count, probabilidad, dias, pasados])
        tmp_df = pd.DataFrame(lista, columns=['N', 'PROB', 'FREQ', 'MEDIA_DIAS', 'ULTIMA_VEZ']) 
        for pos in range(0, 6):
            count = numeros_in_pos[pos].count(numero)
            tmp_df['F'+(str(pos+1))] = count
            tmp_df['P'+(str(pos+1))] = count/len(sorteos)
        df = pd.concat([df, tmp_df])
    df.reset_index(inplace=True, drop=True)
    return df

def obtener_probabilidad(probs, num, idx):
    return probs[num]['P' + str(idx)]

def stad_operaciones(df, campo):
    suma_df = df.groupby(campo).size().reset_index(name='CONTEO')
    suma_df= suma_df.sort_values(by='CONTEO', ascending=False)
    suma_df['CONTEO'] = suma_df['CONTEO'] / df.shape[0]
    probs_dict = suma_df.set_index(campo).to_dict(orient='index')
    df['P_' + campo.upper()] = df[campo].map(lambda num: probs_dict[num]['CONTEO'])
    return df, suma_df

def obtener_combinaciones(numeros, n=6, cols=['N1', 'N2', 'N3', 'N4', 'N5', 'N6']):
    df = pd.DataFrame(combinations(numeros, n), columns=cols)
    return df

def obtener_probs_combinaciones(df, probabilidades, media, moda1, moda2):
    df['SUMA'] = df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6']].sum(axis=1)
    df['RESTA'] = df['N6'] - df['N5'] - df['N4'] - df['N3'] - df['N2'] - df['N1']

    df['D1'] = df['N2'] - df['N1']
    df['D2'] = df['N3'] - df['N2']
    df['D3'] = df['N4'] - df['N3']
    df['D4'] = df['N5'] - df['N4']
    df['D5'] = df['N6'] - df['N5']
    df['SET'] = df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6']].apply(lambda x: set(x), axis=1)
    probs_dict = probabilidades.set_index('N').to_dict(orient='index')
    for i in range(1, 7):
        df['P' + str(i)] = df['N' + str(i)].map(lambda num: obtener_probabilidad(probs_dict, num, i))
    df = stad_operaciones(df, 'SUMA')
    df = stad_operaciones(df, 'RESTA')
    df = stad_operaciones(df, 'D1')
    df = stad_operaciones(df, 'D2')
    df = stad_operaciones(df, 'D3')
    df = stad_operaciones(df, 'D4')
    df = stad_operaciones(df, 'D5')
    df['PROB'] = df[['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P_SUMA', 'P_RESTA', 'P_D1', 'P_D2', 'P_D3', 'P_D4', 'P_D5']].product(axis=1)    
    df.reset_index(inplace=True, drop=True)
    df = df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'PROB', 'SET']]#, 'aciertos_0', 'aciertos_1', 'aciertos_2', 'aciertos_3', 'aciertos_4', 'aciertos_5', 'aciertos_6']].copy()
    #df['ALPHA'] = df['PROB']-moda1
    ##df['ALPHA2'] = df['PROB']-moda2
    #df['ALPHA3'] = df['PROB']-media
    #df['ALPHA'] = df['ALPHA'].abs()
    #df['ALPHA2'] = df['ALPHA2'].abs()
    #df['ALPHA3'] = df['ALPHA3'].abs()    
    #maximo = df['PROB'].max()
    #minimo = df['PROB'].min()
    #df['PROB_N'] = (df['PROB'] - minimo) / (maximo - minimo)
    #df['ALPHA_N'] = (df['ALPHA'] - minimo) / (maximo - minimo)
    #df['ALPHA2_N'] = (df['ALPHA2'] - minimo) / (maximo - minimo)
    #df['ALPHA3_N'] = (df['ALPHA3'] - minimo) / (maximo - minimo)
    
    return df


def obtener_paridad(comb):
    pares = 0
    for x in comb:
        if (x % 2)==0:
            pares +=1
    return pares
    
def genera_valores(df):
    df['SET'] = df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6']].apply(lambda x: set(x), axis=1)
    df['SUMA'] = df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6']].sum(axis=1)
    df['RESTA'] = df['N6'] - df['N5'] - df['N4'] - df['N3'] - df['N2'] - df['N1']
    df['D1'] = df['N2'] - df['N1']
    df['D2'] = df['N3'] - df['N2']
    df['D3'] = df['N4'] - df['N3']
    df['D4'] = df['N5'] - df['N4']
    df['D5'] = df['N6'] - df['N5']
    df['NUM_PARES'] = df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6']].apply(lambda comb: obtener_paridad(comb), axis= 1)
    return df.copy()

def obtener_probs_numeros(df, probabilidades):
    probs_dict = probabilidades.set_index('N').to_dict(orient='index')
    for i in range(1, 7):
        df['P' + str(i)] = df['N' + str(i)].map(lambda num: obtener_probabilidad(probs_dict, num, i))
    return df

def generar_estadisticas(df):
    df = genera_valores(df)
    df, suma_df = stad_operaciones(df, 'SUMA')
    df, resta_df = stad_operaciones(df, 'RESTA')
    df, d1_df = stad_operaciones(df, 'D1')
    df, d2_df = stad_operaciones(df, 'D2')
    df, d3_df = stad_operaciones(df, 'D3')
    df, d4_df = stad_operaciones(df, 'D4')
    df, d5_df = stad_operaciones(df, 'D5')
    df, pares_df = stad_operaciones(df, 'NUM_PARES')
    df.reset_index(inplace=True, drop=True)
    df = df[['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'NUM_PARES', 'SUMA', 'RESTA','D1', 'D2', 'D3', 'D4', 'D5', 'SET', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P_SUMA', 'P_RESTA', 'P_NUM_PARES','P_D1', 'P_D2', 'P_D3', 'P_D4', 'P_D5']]
    return df, suma_df, resta_df, d1_df, d2_df, d3_df, d4_df, d5_df, pares_df

def contar_aciertos(combinacion, serie_sorteo):
    return [len(combinacion.intersection(sorteo)) for sorteo in serie_sorteo]

def rellenar_aciertos(num_aciertos, combinaciones, sorteos):
    for i, combinacion in combinaciones['SET'].items():
        aciertos = contar_aciertos(combinacion, sorteos['SET'])
        conteo = pd.Series(aciertos).value_counts().to_dict()
        for n in num_aciertos:
            if n in conteo:
                combinaciones.at[i, f'aciertos_{n}'] += conteo[n]
        print_secuencia(f'Combinaciones', i)
    return combinaciones

def obtener_aciertos(sorteos, combinaciones):
    num_aciertos = range(7)
    for n in num_aciertos: 
        combinaciones[f'aciertos_{n}'] = 0
    updated_batch = rellenar_aciertos(num_aciertos, combinaciones, sorteos)
    return updated_batch

def ordenar(df, field, asc=True):
    df = df.sort_values(by=field, ascending=asc)
    df.reset_index(inplace=True, drop=True)
    return df.copy()

def comprobar(ganadora, df):
    df['aciertos'] = df['SET'].apply(lambda x: len(x.intersection(ganadora)))
    return df.copy()

def seleccionar(combinaciones, n = 1):
    #combinaciones = combinaciones[combinaciones.aciertos_6==0]
    #combinaciones = combinaciones[combinaciones.aciertos_5==0]
    #combinaciones = combinaciones[combinaciones.PROB > 0]
    resultados = combinaciones.head(n).copy()
    resultados.reset_index(inplace=True, drop=True)
    return resultados

def get_estad(data, estadistica):
    try:
        d = estadistica.loc[data, 'CONTEO']
        return d
    except:
        return 0
    
def mapear_estadisticas(df, freq, estadisticas):
    df = df[(df.N1.isin(freq[freq.P1 > 0]['N'].to_list()))
            & (df.N2.isin(freq[freq.P2 > 0]['N'].to_list()))
            & (df.N3.isin(freq[freq.P3 > 0]['N'].to_list()))
            & (df.N4.isin(freq[freq.P4 > 0]['N'].to_list()))
            & (df.N5.isin(freq[freq.P5 > 0]['N'].to_list()))
            & (df.N6.isin(freq[freq.P6 > 0]['N'].to_list()))].copy()
    df = genera_valores(df)
    print('Generando Valores')
    for key in estadisticas:
        e = estadisticas[key].copy()
        e.set_index(key, drop=True, inplace=True)
        df['P_' + key.upper()] = df[key].map(lambda num: get_estad(num, e))
    return df

def check_metodo(sorteos):
    
    pd.set_option('display.max_rows', 500)
    size = len(sorteos)
    n = 120
    train = sorteos[n:]
    test = sorteos[0:n]
    ganadora_test = test.pop()
    
    print('Extrae ganadora: ', ganadora_test)
    sorteo = 1
    sorteos_df = pd.DataFrame(sorteos, columns=['FECHA', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6'])
    

    while len(test) > 0:
        freq = obtener_frecuencias(train[0:120], n=0, fecha=train[0][0])
        sorteos_df = obtener_probs_numeros(sorteos_df, freq)
        sorteos_df, suma_df, resta_df, d1_df, d2_df, d3_df, d4_df, d5_df, pares_df = generar_estadisticas(sorteos_df)
        sorteos_df['PROB1'] = sorteos_df[['P1', 'P2', 'P3', 'P4', 'P5', 'P6']].product(axis=1)
        sorteos_df['PROB2'] = sorteos_df[['P_SUMA', 'P_RESTA', 'P_NUM_PARES', 'P_D1', 'P_D2', 'P_D3', 'P_D4', 'P_D5']].product(axis=1)
        sorteos_df['PROB'] = sorteos_df[['PROB1', 'PROB2']].product(axis=1)
        sorteos_df = sorteos_df[sorteos_df.PROB > 0].copy()
        media = sorteos_df['PROB'].mean()
        moda = sorteos_df['PROB'].mode()
        moda1= moda[0]
        probabilidades = {'SUMA':suma_df, 'RESTA':resta_df, 'D1':d1_df, 'D2':d2_df, 'D3':d3_df, 'D4':d4_df, 'D5':d5_df , 'NUM_PARES': pares_df }
        num1, num2, n1, n2 = generar__numeros(freq)
        print(f'{len(num1)} Obtenidos en la lista 1 - {get_date()} ' )
        print(f'{len(num2)} Obtenidos en la lista 2 - {get_date()}' )
        #-------
        df1 = obtener_combinaciones(num1)
        print(f'{df1.shape[0]} Combinaciones en la lista 1 - {get_date()} ' )
        df1 = obtener_probs_numeros(df1, freq)
        df1 = mapear_estadisticas(df1, freq, probabilidades)
        df1['PROB1'] = df1[['P1', 'P2', 'P3', 'P4', 'P5', 'P6']].product(axis=1)
        df1['PROB2'] = df1[['P_SUMA', 'P_RESTA', 'P_NUM_PARES', 'P_D1', 'P_D2', 'P_D3', 'P_D4', 'P_D5']].product(axis=1)
        df1['PROB'] = df1[['PROB1', 'PROB2']].product(axis=1)
        df1 = df1[df1.PROB2 > 0].copy()
        df1['PROB'] = (df1['PROB2'] - df1['PROB1'] - media).abs()
        df1 = df1[['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'SET', 'PROB', 'PROB1', 'PROB2']].copy()
        #df1 = df1[df1.N1.isin([n1,n2])].copy()
        df1.sort_values(by=['PROB'], ascending=[True], inplace=True)
        df1.reset_index(drop=True, inplace=True)
        df1 = comprobar(set(ganadora_test[1:]), df1)
        df1 = df1.head(1000).copy()
        #--------------------------------------------------
        df2 = obtener_combinaciones(num2)
        print(f'{df2.shape[0]} Combinaciones en la lista 2 - {get_date()} ' )
        df2 = obtener_probs_numeros(df2, freq)
        df2 = mapear_estadisticas(df2, freq, probabilidades)
        df2['PROB1'] = df2[['P1', 'P2', 'P3', 'P4', 'P5', 'P6']].product(axis=1)
        df2['PROB2'] = df2[['P_SUMA', 'P_RESTA', 'P_NUM_PARES', 'P_D1', 'P_D2', 'P_D3', 'P_D4', 'P_D5']].product(axis=1)
        df2['PROB'] = df2[['PROB1', 'PROB2']].product(axis=1)
        df2 = df2[['N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'SET', 'PROB', 'PROB1', 'PROB2']].copy()
        df2 = df2[df2.PROB2 > 0].copy()
        df2['PROB'] = (df2['PROB2'] - df2['PROB1'] - media).abs()
        df2.sort_values(by=['PROB'], ascending=[True], inplace=True)
        df2.reset_index(drop=True, inplace=True)
        df2 = comprobar(set(ganadora_test[1:]), df2)
        df2 = df2.head(1000).copy()

        df1.reset_index(drop=False, inplace=True)
        df2.reset_index(drop=False, inplace=True)
        df1.sort_values(by=['index'], ascending=False, inplace=True)
        df2.sort_values(by=['index'], ascending=False, inplace=True)
        df1.reset_index(drop=True, inplace=True)
        df2.reset_index(drop=True, inplace=True)
        df1 = df1.head(100).copy()
        df2 = df2.head(100).copy()
        
        numeros_df = df1['SET'].to_list() 
        lista_numeros = []
        grupos = []
        count_grupos = []
        for s in numeros_df:
            lista_numeros += list(s)
        for n in lista_numeros:
            if not n in grupos:
                grupos.append(n)
                count_grupos.append([n, lista_numeros.count(n)])
        count_grupos.sort(key = lambda x: x[1], reverse=True)

        num3 = [n[0] for n in count_grupos]
        df3 = obtener_combinaciones(num3, 3, cols=['N1', 'N2', 'N3'])
        df3['SET'] = df3[['N1', 'N2', 'N3']].apply(lambda x: set(x), axis=1)
        df3 = obtener_aciertos(df1, df3)
        df3.sort_values(by=['aciertos_3'], ascending=[True], inplace=True)
        print(df3)
        input('...')
        
        numeros_df = df2['SET'].to_list() 
        lista_numeros = []
        grupos = []
        count_grupos = []
        for s in numeros_df:
            lista_numeros += list(s)
        for n in lista_numeros:
            if not n in grupos:
                grupos.append(n)
                count_grupos.append([n, lista_numeros.count(n)])
        count_grupos.sort(key = lambda x: x[1], reverse=True)

        num3 = [n[0] for n in count_grupos]
        df3 = obtener_combinaciones(num3, 3, cols=['N1', 'N2', 'N3'])
        df3['SET'] = df3[['N1', 'N2', 'N3']].apply(lambda x: set(x), axis=1)
        df3 = obtener_aciertos(df2, df3)
        df3.sort_values(by=['aciertos_3'], ascending=[True], inplace=True)
        print(df3)
        input('...')

        
        aciertos1 = df1[df1.aciertos >= 3]
        aciertos2 = df2[df2.aciertos >= 3]
        print(aciertos1)
        print(aciertos2)
        if (aciertos1.shape[0] + aciertos2.shape[0] > 0):
            print(aciertos1.shape[0])
            print(aciertos2.shape[0])
            input('....')
        #-----
        
        
def generar__numeros(freq):
    numeros_lista = []
    n1, n2 = 0, 0
    for i in range(1, 7):
        freq.sort_values(by=['P'+str(i)], ascending=False, inplace=True)
        n = freq[(freq['P'+str(i)] > 0) & ~(freq['N'].isin(numeros_lista))]
        n = n[['N', 'FREQ', 'MEDIA_DIAS', 'ULTIMA_VEZ', 'P'+str(i)]].copy()
        n['P'] = (n['P'+str(i)]*(n['ULTIMA_VEZ']-n['MEDIA_DIAS']).abs())
        n.sort_values(by=['P'], ascending=[False], inplace=True)
        numeros_lista += n['N'].to_list()[0:4]
        if (i==1):
            n1, n2 = numeros_lista[0],numeros_lista[1]
        numeros_lista = list(set(numeros_lista))
    diff = set(list(range(1,50))).difference(set(numeros_lista))
    return numeros_lista, list(diff), n1, n2
