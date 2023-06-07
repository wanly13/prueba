import math

def tfidf(tf , archivos):
    lista = {}
    it = 0
    for i in tf:
        for k in i:
            wtfidf = math.log(1 + i[k]) * math.log(len(tf)/df(k, tf))
            if k in lista:
                lista[k] = str(lista[k]) + ";" + str(archivos[it]) + "," + str(wtfidf)             
            else:
                lista[k] = str(archivos[it]) + "," + str(wtfidf)
        it += 1            
        if(it % 5 == 0):
            writeblock(lista, it/5)
            lista = {}
    
    writeblock(lista, math.ceil(it/5))


def writeblock(lista, c):
    nombre = "index" + str(int(c)) + ".txt"
    with open(nombre, 'a', encoding='utf-8') as data:
        for k in lista:
            data.write(k + ':'+ lista[k] + '\n')


def df(word, lista):
    c = 0
    for i in lista:
        if word in i:
            c += 1
    return c