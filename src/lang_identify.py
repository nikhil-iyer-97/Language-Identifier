import re
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk import trigrams
from nltk import bigrams
import pickle

languages = ["deu","fra","eng","spa","ita","nld","por","hun","swe","fin","pol","kaz","rus","dan","lat","hin","cmn",\
             "jpn","ara","urd","ukr","ind","mal","afr","hrv","heb","isl","kor","tha","bul"]

lang_dict = {}
with open("../data/lang_dict.p",'rb') as f:
    lang_dict = pickle.load(f)

def clean_text(text):
    sent = re.sub("[^\p{Sc}\p{So}\p{Mn}\p{P}\p{Z}À-ÿ\D+']"," ",text).replace('\n','').replace('\t',' ').replace('|',' ').replace('.',' ')\
            .replace('。',' ').replace(',',' ').replace('!',' ').replace('?',' ').replace(":",' ').replace(';',' ')\
            .replace('(','').replace(')','').replace('"','').replace('!','').replace('-','').replace('*','')
    return sent

def calc_dist(key,inp_table):
    dist = 0
    max_int = 1e9
    for ngram in inp_table.keys():
        #print(ngram)
        cur_dict = lang_dict[key]
        if ngram in cur_dict:
            idx1 = cur_dict[ngram]
            idx2 = inp_table[ngram]
            dist += abs(idx1-idx2)
        else:
            dist += max_int
    return dist


fileloc = " "
fo = open(fileloc,"r+")
inp = fo.read()
print(inp)
inp = clean_text(inp)
#inp = input()
tokens = word_tokenize(inp)
for i in range(len(tokens)):
    tokens[i] = tokens[i].lower()
    tokens[i] = "|" + tokens[i] + "|"

profile= FreqDist()
for t in tokens:
    token_bigrams = bigrams(list(t))
    token_trigrams = trigrams(list(t))

    for cur_bigram in token_bigrams:
        cur_bigram = "".join(cur_bigram)
        if cur_bigram in profile:
            profile[cur_bigram] += 1
        else:
            profile[cur_bigram] = 1

    for cur_trigram in token_trigrams:
        cur_trigram = "".join(cur_trigram)
        if cur_trigram in profile:
            profile[cur_trigram] += 1
        else:
            profile[cur_trigram] = 1


most_common = profile.most_common(20000)
new_list = []
for x in most_common:
    new_list.append(x[0])
inp_table = {}
idx = 0
for w in new_list:
    inp_table[w] = idx
    idx+=1

dist_measure={}
for key in lang_dict.keys():
    dist_measure[key] = calc_dist(key,inp_table)

lang= ""
min_dist= 1e18
for key in lang_dict.keys():
    if(dist_measure[key] < min_dist):
        lang = key
        min_dist = dist_measure[key]

print("Original is eng,  The input is written in",lang,"\n")
