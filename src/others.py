
from nltk.stem.snowball import SnowballStemmer
from collections import Counter
import nltk
from  clean_twets import remove_URL, signosp , strip_emoji ,remove_emojis, stoplist

def df_ind(word, ind):
    line = ind[word]
    line = line.split(';')
    return len(line)

def parser(line):
    i = line.split(':')
    return i

def readFile(name):
    ans = []
    stemmer = SnowballStemmer('spanish')
    palabras = nltk.word_tokenize(remove_URL(signosp(strip_emoji(remove_emojis(name))).lower()))
    for token in palabras:
        word = stemmer.stem(token)
        if word not in stoplist:
            ans.append(word)
    return Counter(ans)

def readFile2(name):
    ans = []
    palabras = nltk.word_tokenize(remove_URL(signosp(strip_emoji(remove_emojis(name))).lower()))
    for token in palabras:
        if token not in stoplist:
            ans.append(token)
    return ans

def merge(lista):
    ans = Counter()
    for i in lista:
        ans += i
    return ans