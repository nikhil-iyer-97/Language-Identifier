import pandas as pd
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk import trigrams
from nltk import bigrams

languages = ["deu","fra","eng","spa","ita","nld","por","hun","swe","fin","pol","kaz","rus","dan","lat","hin","cmn",\
             "jpn","ara","urd","ukr","ind","mal","afr","hrv","heb","isl","kor","tha","bul"]

def clean_text(text):
    sent = re.sub("[^\p{Sc}\p{So}\p{Mn}\p{P}\p{Z}À-ÿ\D+']"," ",text).replace('\n','').replace('\t',' ').replace('|',' ').replace('.',' ')\
            .replace('。',' ').replace(',',' ').replace('!',' ').replace('?',' ').replace(":",' ').replace(';',' ')\
            .replace('(','').replace(')','').replace('"','').replace('!','').replace('-','').replace('*','')
    return sent

data = pd.read_csv("../data/dataset.csv")

corpus_sents = {}
for lang in languages:
    df =  data.loc[data['lang'] == lang]
    lis = []
    for sent in df.sentences:
        sent = clean_text(sent)
        lis.append(sent)
    corpus_sents[lang] = lis

lang_dict = {}
for key in corpus_sents.keys():
    tokens = []
    for sent in corpus_sents[key]:
        tokens+= word_tokenize(sent)
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
        tokens[i] = "|" + tokens[i]+ "|"

    profile = FreqDist()
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
    idx = 0
    lang_table = {}
    for w in new_list:
        lang_table[w] = idx
        idx+=1
    lang_dict[key] = lang_table

with open("../data/lang_dict.p", "wb") as f:
    pickle.dump(lang_dict, f)
