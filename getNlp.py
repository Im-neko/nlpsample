#-*- coding:utf-8 -*-
import codecs
import csv
import re
from natto import MeCab
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def nlp(data):
    nm = MeCab() # nmというMeCabクラスのインスタンスを作成
    points = 0 # 文章全体の評価
    negaposi_dic = getNegaPosiDic() # 評価データの読み込み(さっき作った関数を呼び出している。)
    sentenses = re.split("[。！!♪♫★☆>?？（）w]", data)  # 一文ごとに分ける
    try:
        for sentense in sentenses: # 文の数だけ繰り返す
            negaposi = 0
            result_all = nm.parse(sentense) # 形態素解析して品詞分解をしている。
            result_words = result_all.split("\n")[:-1]  # 単語ごとに分ける
            for word in result_words:
                try:
                    word_toarray = re.split('[\t,]', word)
                    if word_toarray[7] in negaposi_dic:
                        negaposi = int(negaposi_dic[word_toarray[7]])  # その文のネガポジ
                        print(word_toarray[7],negaposi_dic[word_toarray[7]], flush=True) # 評価リストに入っていたワードとその評価
                except Exception as e:
                    print('%r' % e, flush=True)
            points += negaposi # 文章全体の評価に加算
    except Exception as e:
        print('%r' % e, flush=True)
        print(data, flush=True)
    return points # 文章全体の値を返す。

def getNegaPosiDic():
    with codecs.open(os.path.join(__location__, "./dataset/yougen.csv"), 'r', 'utf-8') as f_in:
        reader = csv.reader(f_in, delimiter=',', lineterminator='\n')
        negaPosiDic = {}
        for i, x in enumerate(reader):
            y = x[0].split(" ")
            negaPosiDic[y[1]] = y[0]
    with codecs.open(os.path.join(__location__, "./dataset/noun.csv"), 'r', 'utf-8') as f_in:
        reader = csv.reader(f_in, delimiter=',', lineterminator='\n')
        for i, x in enumerate(reader):
            y = x[0].split(" ")
            negaPosiDic[y[1]] = y[0]
    return negaPosiDic

if __name__=='__main__':
    data = ""
    while True:
        t = input()
        if t == '':
            break
        data = data + str(t)
    print(nlp(data))
