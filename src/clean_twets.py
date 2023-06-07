#import os
import json
#import nltk
#from nltk.stem.snowball import SnowballStemmer
#from collections import Counter
#import math
import re
import emoji
import operator
from collections import OrderedDict
from others import readFile , merge
from inverted_index import tfidf
from search import input_directory , stopListTXT , archivos
#input_directory = "dataset_clean"
#curpath = os.path.abspath(os.curdir)

punc = [ "¡", "«", "»", ".", ",", ";", "(", ")", ":", "@", "RT", "#", "|", "¿", "?", "!", "https", "$", "%", "&", "'", "''", "..", "...", '\'', '\"' ]
with open(stopListTXT) as file:
    stoplist = [line.lower().strip() for line in file]
stoplist += ["«", "»", ".", ",", ";", "(", ")", ":", "@", "RT", "#", "|", "?", "!", "https", "$", "%", "&", "'", "''", "..", "...", '\'', '\"' ]

#archivos = os.listdir(input_directory)





def signosp(word):
    for x in word:
        if x in punc:
            word = word.replace(x, "")
    return word

""" def merge(lista):
    ans = Counter()
    for i in lista:
        ans += i
    return ans """

def json_tweets_to_dic():
    tf = []
    for filename in archivos:
        lista = []
        if filename.endswith(".json") :
            with open(input_directory + '\\' + filename, 'r', encoding='utf-8') as all_tweets:
                all_tweets_dictionary = json.load(all_tweets)
                for tweet in all_tweets_dictionary:
                    temp = readFile(all_tweets_dictionary[tweet])
                    lista.append(temp)
                tf.append(merge(lista))
    tfidf(tf , archivos)
  
      
""" def tfidf(tf):
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
    
    writeblock(lista, math.ceil(it/5)) """

""" def writeblock(lista, c):
    nombre = "index" + str(int(c)) + ".txt"
    with open(nombre, 'a', encoding='utf-8') as data:
        for k in lista:
            data.write(k + ':'+ lista[k] + '\n') """
                

""" def df(word, lista):
    c = 0
    for i in lista:
        if word in i:
            c += 1
    return c """

def remove_URL(sample):
    return re.sub(r"http\S+", "", sample)


def give_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u200b"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\u2066"
        u"\u2069"
        u"\u0144"
        u"\u0148"
        u"\u2192"
        u"\u2105"
        u"\u02dd"
        u"\u0123"
        u"\u0111"
        u"\u013a"
        u"\u2193"
        u"\u2191"
        u"\u0307"
        u"\u0435"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def strip_emoji(text):
    new_text = re.sub(emoji.get_emoji_regexp(), r"", text)
    return new_text

""" def readFile(name):
    ans = []
    stemmer = SnowballStemmer('spanish')
    palabras = nltk.word_tokenize(remove_URL(signosp(strip_emoji(remove_emojis(name))).lower()))
    for token in palabras:
        word = stemmer.stem(token)
        if word not in stoplist:
            ans.append(word)
    return Counter(ans) """


""" def parser(line):
    i = line.split(':')
    return i """

ind = {}  

""" def df_ind(word, ind):
    line = ind[word]
    line = line.split(';')
    return len(line) """

""" def readInverted():
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
    return ind """
    
""" def search(query, k):
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
    return orderedDic[:k] """

""" def readFile2(name):
    ans = []
    palabras = nltk.word_tokenize(remove_URL(signosp(strip_emoji(remove_emojis(name))).lower()))
    for token in palabras:
        if token not in stoplist:
            ans.append(token)
    return ans """

""" def find_tweetids(query, k):
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
    return lista   """
           