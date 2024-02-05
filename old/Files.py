from datetime import datetime

def leerSorteos(nameFile: str):
    file_out  = open('C:\\sandbox\\result.txt', 'a+')
    sorteosFile = open(nameFile, 'r+')    
    line :str = sorteosFile.readline()
    listaSorteos = []
    while line:
        if line != '':
            acertante = line.strip().split(',')
            try:
                fecha = datetime.strptime(acertante[0], '%d/%m/%Y').date().strftime('%m/%d/%Y')
                sorteo = [s for s in acertante[1:7] if s]
                file_out.write(",".join([fecha]+sorteo)+'\n')
            except:
                pass
        line = sorteosFile.readline()
    file_out.close()
    return listaSorteos
leerSorteos('bonoloto.csv')
leerSorteos('bonoloto2.csv')