import os
import math
import nltk
import json
from others import readFile , readFile2 , df_ind

input_directory = "dataset_clean"
stopListTXT = 'stoplist.txt'
curpath = os.path.abspath(os.curdir)
archivos = os.listdir(input_directory)
ind = {}  

def parser(line):
    i = line.split(':')
    return i

def readInverted():
    path = "index"
    cont = 1
    while(True):
        pat = path + str(cont)+".txt"
        if os.path.exists(pat):
            with open(pat, 'r', encoding="ISO-8859-1") as f:
                for index, line in enumerate(f):
                    pair = parser(line[:len(line)-2])
                    if pair[0] in ind:
                        ind[pair[0]] = str(ind[pair[0]]) + ";" + str(pair[1])          
                    else:
                        ind[pair[0]] = str(pair[1])
            cont += 1
        else:
            break
    return ind


def search(query, k):
    tf = readFile(query)
    dic = {}
    inverted = readInverted()
    scores = {}
    lenght1 = {}
    for i in archivos:
        scores[i] = 0
        lenght1[i] = 0
    lenght2 = 0
    for i in tf:
        wtfidf = math.log(1 + tf[i]) * math.log(len(archivos)/df_ind(i, inverted))
        dic[i] = wtfidf
        lenght2 = lenght2 + wtfidf**2
        values = inverted[i].split(';')
        for j in values:
            j = j.split(',')
            lenght1[j[0]] = lenght1[j[0]] + float(j[1])**2
            scores[j[0]] = scores[j[0]] + float(j[1])*wtfidf
    lenght2 = lenght2**0.5
    for i in lenght1:
        if lenght1[i] != 0:
            lenght1[i] = lenght1[i]**0.5
    for i in scores:
        if lenght1[i] != 0:
            scores[i] = scores[i]/(lenght1[i]*lenght2)
    orderedDic = sorted(scores.items(), key=lambda it: it[1], reverse=True)
    return orderedDic[:k]



def find_tweetids(query, k):
    documentos = search(query, k)
    palabras = readFile2(query)
    lista = []
    ct = 0
    for i in documentos:      
        with open(input_directory + '\\' + i[0], 'r', encoding='utf-8') as all_tweets:
            all_tweets_dictionary = json.load(all_tweets)
            for w in palabras:
                for tweet in all_tweets_dictionary:               
                    temp = all_tweets_dictionary[tweet]            
                    if temp.find(w) != -1:
                        lista.append((tweet, all_tweets_dictionary[tweet]))
                        ct += 1                   
                    if ct == k: break 
                if ct == k: break
        if ct == k: break    
    return lista  