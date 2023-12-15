sorteosFile = open('bonoloto.csv', 'r')
line :str = sorteosFile.readline()
todos = []
contador = 0
while line:
    line = sorteosFile.readline()
    if line != '':
        acertante = line.strip().split(',')
        sorteos = [int(s) for s in acertante[1:8] if s]
        todos.append(sorteos)
d = open('data.txt', 'a+')
for x in todos:
    d.write(",".join([str(n) for n in  x])+"\n")
d.close()