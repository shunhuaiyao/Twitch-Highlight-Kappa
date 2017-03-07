import jieba
from collections import defaultdict
import operator
import io
import os
import WordCloud
jieba.set_dictionary('./extra_dict/dict.txt.big')
jieba.load_userdict("./extra_dict/userdict.txt")

TIME_INTERVAL = 10 #sec
DIMENSIONS = 200

stop_words = [' ', '\n', '\t']
fr_sw = open('./extra_dict/stop_words.txt','r',encoding='utf-8-sig')
for word in fr_sw:
    word = word.rstrip()
    stop_words.append(word)
fr_sw.close()

        

def getChat(videoId, video_type):
    import time, json, requests, sys
    if(video_type=='h'):
        video_type = 'highlight'
    elif(video_type=='v'):
        video_type = 'VoD'
    #videoId = input('Enter the video ID: ')
    videoId = videoId
    #API url
    url = 'https://rechat.twitch.tv/rechat-messages'

    #Use start=0 to get the begin and end time.
    url1 = url + '?' + 'start=0&video_id=v' +  videoId
    re = requests.get(url1).json()
    detail = re['errors'][0]['detail'].split(' ')
    start, stop = int(detail[4]), int(detail[6])
    total = stop - start

    messageIds = []

    file_name = video_type+'_'+videoId + '.txt'
    fw = open('./data/'+file_name, 'w', encoding='utf-8-sig')
    # Download all the messages from chatroom for time=start to end.
    timestamp = start
    print('Start downloading '+video_type+' '+videoId+'... Please wait for a while.')
    while timestamp <= stop:
        url2 = url + '?start=' + str(timestamp) + '&video_id=v' + videoId

        re = requests.get(url2).json()
        try:
            data = re['data']
        except:
            print("No chats for this video")
            return None

        timestamp = timestamp + 1

        for datum in data:
            if not any(datum['id'] in messageId for messageId in messageIds):
                messageIds.append(datum['id'])
                date    = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(datum['attributes']['timestamp']/1000.))
                user  = datum['attributes']['from']
                message    = datum['attributes']['message']
                progress = timestamp - start
                percentage = round(progress*100 / float(total), 2)
                percentage = 100.0 if percentage > 100.0 else percentage
                sys.stdout.write('Downloading... (' + str(percentage) + '%)\r')
                sys.stdout.flush()
                #fw.write(date + ' ' + user + ': ' + message + '\n')
                fw.write(str(int(datum['attributes']['timestamp'])//1000) + ' ' + user + ': ' + message + '\n')
                timestamp = int(datum['attributes']['timestamp']/1000) #Change timestamp to the last message of this time frame to improve performance.
    fw.close()
    print('Finished downloading ' + videoId + '\n')
    WordCloud.PrintTFIDFTotxt(videoId)
    return start


def split_words_all(file_name):
    # encoding=utf-8
    
    fr = open('./data/'+file_name,'r',encoding="utf-8-sig")
    total_message = 0
    hashDict = defaultdict(int)
    for line in fr:
        total_message += 1
        line = line.split(' ')[2:]
        data = ' '.join(line)
        seg_list = jieba.cut(data)
        line_word_set = set([])
        for word in seg_list:

            word = check_word(word)
            if(word is None):
                continue
            line_word_set.add(word)
        for word in line_word_set:
            hashDict[word] += 1/(len(line_word_set))
    fr.close()
    hashDict = dictToList(hashDict)
    return hashDict
'''
def split_words_time(chats):
    # encoding=utf-8
    hashDict = defaultdict(int)
    for chat in chats:
        seg_list = jieba.cut(chat)
        line_word_set = set([])
        for word in seg_list:
            word = check_word(word)
            line_word_set.add(word)
        for word in line_word_set:
            hashDict[word] += 1
    hashDict = dictToList(hashDict)
    return hashDict
'''
def new_split_words_time(chats, user_dict, total_messsage):
    # encoding=utf-8
    import math
    total = 0
    for data in chats:
        user = data[0]
        total += 1/user_dict[user]

    hashDict = defaultdict(int)
    for data in chats:
        chat = data[1]
        user = data[0]
        
        weight = 1/user_dict[user]
        weight = weight/total
        


        seg_list = jieba.cut(chat)
        line_word_set = set([])
        for word in seg_list:
            word = check_word(word)
            line_word_set.add(word)
        for word in line_word_set:
            hashDict[word] += 1*weight
    hashDict = dictToList(hashDict)
    return hashDict

def dictToList(hashDict):
    hashDict = list(reversed(sorted(hashDict.items(), key=lambda t:t[1])))
    hashDict = list(zip(*hashDict))
    return hashDict

def check_word(word):
    if(word in stop_words):
        return None
    if(word.find('+1')>-1):
        word = '+1'
    elif(word.find('+2')>-1):
        word = '+2'
    elif(word.find('87')>-1):
        word = '87'
    elif(word.find('22')>-1):
        word = '222'
    elif(word.find('44')>-1):
        word = '444'
    elif(word.find('66')>-1):
        word = '666'
    elif(word.find('77')>-1):
        word = '777'
    elif(word.find('88')>-1):
        word = '888'
    elif(word.find('GG')>-1 or word.find('gg')>-1):
        word = 'GG'
    elif(word.find('RR')>-1 or word.find('rr')>-1):
        word = 'RRR'
    return word

def get_word_table(videoId):
    from jieba import analyse
    fr = open('./data/VoD_'+videoId +'.txt','r', encoding='utf-8-sig')
    str_list = []
    hashDict = defaultdict(int)
    for line in fr:
        data = line.split(' ')
        user = data[1]
        hashDict[user] += 1
        message = ' '.join(data[2:])
        str_list.append(message)
    fr.close()
    total_messsage = len(str_list)
    fullText = ' '.join(str_list)

    TFIDF = jieba.analyse.extract_tags(fullText, topK=DIMENSIONS,withWeight=True)
    TFIDF = list(zip(*TFIDF))
    table_words = TFIDF[0]
    table_weights = TFIDF[1]
    table = (table_words, table_weights)
    
    return table, hashDict, total_messsage

def extract_features(VoD, highlight_time):
    if(highlight_time is not None):
        fw = open('./data/'+VoD+'_training_features.txt', 'w', encoding='utf-8-sig')
    else:
        fw = open('./data/'+VoD+'_testing_features.txt', 'w', encoding='utf-8-sig')

    data = []
    labels = []
    _time = []
    table, user_dict, total_messsage = get_word_table(VoD)
    fr = open('./data/VoD_'+VoD+'.txt','r', encoding='utf-8-sig')
    content = fr.readlines()
    fr.close()
    i = 0
    start_sec = -1
    chats = []
    prev_total_users = 1
    prev_growth_rate = 0
    fw_sum_users = open('sum_of_users_'+VoD+'.txt', 'w')
    user_set = set([])
    while(i<len(content)):
        sec = int(content[i].split(' ')[0])
        user = content[i].split(' ')[1]
        user_set.add(user)
        if((sec-start_sec) >= TIME_INTERVAL):
            if(chats):
                #raw_features = split_words_time(chats)
                raw_features = new_split_words_time(chats, user_dict, total_messsage)
                data_object = get_features(table, raw_features)
                total_users = len(user_set)
                growth_rate = (total_users-prev_total_users)/prev_total_users
                data_object.append(growth_rate)
                data_object.append(prev_growth_rate)
                data_object.append(len(chats))
                prev_growth_rate = growth_rate
                #print(sum(data_object))
                fw.write(str(sum(data_object))+'\n')
                data.append(data_object)
                _time.append(start_sec)
                if(highlight_time is not None): #Training
                    is_hightlight = check_highlight(start_sec, highlight_time)
                    labels.append(is_hightlight)
                    fw_sum_users.write(str(start_sec)+' '+str()+'\n')
                    prev_total_users = total_users
                    user_set = set([])
                    
                chats = []
            remainder = sec%TIME_INTERVAL
            start_sec = sec-remainder
            first = True
        if(first):
            fw.write("---"+str(start_sec)+"----\n")
            first = False
        chat = content[i].split(' ')[2].rstrip()
        if(len(chat)>0):
            chats.append((user, chat))
            #chats.append(chat)
        i = i + 1
    fw.close()
    fw_sum_users.close()
    if(highlight_time is not None):
        return _time, data, labels
    else:
        return _time, data

def get_features(table, raw_features):
    table_words, table_weights = table[0], table[1]
    words, frequencies = raw_features
    features = [0]*len(table_words)
    for i in range(len(table_words)):
        try:
            index = words.index(table_words[i])
            features[i] = frequencies[index]*table_weights[i]
        except:
            continue
    return features

def train_model(clf, data, labels):
    clf.fit(data, labels)
    print('Done training')

def check_highlight(start_time, highlight_time):
    for highlight in highlight_time:
        start_highlight = highlight[0]
        end_highlight = highlight[1]
        if(start_time>=start_highlight and start_time<=end_highlight):
            return True
    return False

def get_highlight_time(file_name):
    highlight_time = []
    fr = open('./data/'+file_name, 'r', encoding='utf-8-sig')
    for line in fr:
        line = line.split(' ')
        start, end = int(line[0]), int(line[1])
        highlight_time.append((start, end))
    fr.close()
    return highlight_time
def get_frame_secs():
    return TIME_INTERVAL