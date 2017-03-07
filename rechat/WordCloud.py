# -*- coding=utf-8 -*-
import jieba
import json
import operator
import sys
from collections import OrderedDict
from operator import itemgetter
from collections import defaultdict
import jieba.analyse
import sys


jieba.set_dictionary('./extra_dict/dict.txt.big')
#jieba.load_userdict("./extra_dict/userdict.txt")

def DataPreprocessing(path):
    textcontent = []
    time = []
    user = []
    f = open(path, 'r', encoding='utf-8-sig')
    for line in f:
        temp = line.replace('\n', '').split(" ", 1)
        #append to time array
        time.append(temp[0])
        content = temp[1].replace(':', '').replace('~','').replace('~','').split(" ", 1)
        user.append(content[0])
        content[1] = (content[1].replace(' ', '').replace('█','').replace('▇','').replace('▄','').replace('⊙','').replace('▄','')
                                   .replace('▲', '').replace('◥', '').replace('▅', '').replace('▂', '').replace('░', '')
                                   .replace('▒', '').replace('༽', '').replace('▌', '').replace('⎠', '').replace('◤', '')
                                   .replace('༼', '').replace('◕', '').replace(']', '').replace('【', '').replace('】', '')
                                   .replace('-', '').replace('>', '').replace('<', '').replace('ー', '').replace('︻','')
                                   .replace('つ', '').replace('▃', '').replace('￣', '').replace('▀', '').replace('▐','').replace('.','')
                                   .replace('=','').replace('～','').replace('~','').replace('ミ','').replace('°','').replace('╤','')
                                   .replace('ʕ','').replace('╦','').replace('╱','').replace(')','').replace('⎝','').replace('─','') )
        textcontent.append(content[1])
    return textcontent

'''
TFIDF用法jieba.analyse.extract_tags

jieba.analyse.extract_tags（sentense,topK = 20,withWeight = False,allowPOS =（））
    ＊ topK為待提取的文本
    ＊ TOPK為返回幾個TF / IDF權重最大的關鍵詞，默認值為20
    ＊ withWeight為是否一併返回關鍵詞權重值，默認值為假
    ＊ allowPOS僅包括指定詞性的詞，默認值為空，即不篩選

我的Fulltext是用結巴分詞後的詞用一個space組合在一起，然後集結成一個很大的文本
算出來的TF-IDF假設有要回傳權重（withWeight）的話，就會是一個Tuple
'''
def GetTFIDF(FullText,Number):
    TFIDF = jieba.analyse.extract_tags(FullText, topK=Number,withWeight=True)
    keyWordsDict = {keyword[0]:keyword[1]*10 for keyword in TFIDF}
    return keyWordsDict


def GetFullText(textcontent):
    Fulltext = ""
    hashDict = defaultdict(int)
    for sentense in textcontent:
        #print(sentense)
        seglist = jieba.cut(sentense, cut_all=False)
        tempSentense = ''
        for item in seglist:
            if(item.count('444')>1):
                item = '444'
            elif(item.count('66')>1):
                item = '666'
            elif(item.count('77')>1):
                item = '777'
            elif(item.count('88')>1):
                item = '88'
            elif(item.count('XDD')>1):
                item = 'XD'
            elif(item.count('GG')>1):
                item = 'GG'
            elif(item.count('gg')>1):
                item = 'gg'
            elif(item.count('RR')>1):
                item = 'RRRR'
            elif(item.count('rr')>1):
                item = 'RRRR'
            elif(item.count('87')>=1):
                item = '87'
            elif(item.count('BabyRage')>=1):
                item = 'BabyRage'
            elif(item.count('SwiftRage')>=1):
                item = 'SwiftRage'
            elif(item.count('PeterZarollTie')>=1):
                item = 'PeterZarollTie'
            elif(item.count('BibleThump')>=1):
                item = 'BibleThump'       
            elif(item.count('MingLee')>=1):
                item = 'MingLee'  
            elif(item.count('godtoneGOD')>=1):
                item = 'godtoneGOD'                       
            tempSentense += item

            ##---------計算出現的次數
            hashDict[item] +=1
        ###----把每個詞用空白組合在一起當作文本，之後要來做TF-IDF
        Fulltext += tempSentense+" "
    return Fulltext

def PrintTFIDFTotxt(VoD):
    path = './data/VoD_'+VoD+'.txt'
    print(path)
    textcontent = DataPreprocessing(path)
    Fulltext = GetFullText(textcontent)
    #print(Fulltext)
    TFIDF = GetTFIDF(Fulltext,50)
    print (TFIDF)
    keywordfilename = './data/'+VoD+'_keyword.txt'

    with open(keywordfilename, 'w',encoding='utf-8') as f:
         json.dump(TFIDF, f, ensure_ascii=False)

# VoD = '108244967'
# PrintTFIDFTotxt(VoD)
#sortedTuple = [(k, hashDict[k]) for k in sorted(hashDict, key=hashDict.get, reverse=False)]
