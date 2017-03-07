#!flask/bin/python
from flask import Flask
from flask import render_template
import os
import json
import requests
import MySQLdb
from webob import Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/v1.0/setVODInfo/<string:id>', methods=['GET'])
def set_vod_info(id):
    url = "https://api.twitch.tv/kraken/videos/v"+id
    VODBody = requests.get(url, headers = { 'Client-ID':'jwwt96ysrnu4kc0cl4v65gecxqxr9iw' }).json()
    VODInfo = { "title" : VODBody['title'],
    "date" : VODBody['recorded_at'],
    "preview_url" : VODBody['preview'] ,
    "author" : VODBody['channel']['display_name'] + "(" + VODBody['channel']['name'] +")"
    }
    db = MySQLdb.connect(host="140.114.77.126", user="hsnl", passwd="hsnl33564", db="twitchhl",charset='utf8')
    cursor = db.cursor()
    command = "INSERT INTO `videoinfo`(id,title,author,preview_url,video_time) VALUES ("+id+",\""+VODInfo['title']+"\",\""+VODInfo['author']+"\",\""+VODInfo['preview_url']+"\",\""+VODInfo['date']+"\")"
    cursor.execute(command)
    db.commit()
    return Response(content_type='application/json; charset=utf-8', body="OK")

@app.route('/api/v1.0/getlatestVOD', methods=['GET'])
def get_vod_info1():
    VODInfo = []
    db = MySQLdb.connect(host="140.114.77.126", user="hsnl", passwd="hsnl33564", db="twitchhl",charset='utf8')
    cursor = db.cursor()
    command = "SELECT * FROM `videoinfo` ORDER BY PRIMARY_ID DESC LIMIT 6"
    cursor.execute(command)
    db.commit()
    result_set = cursor.fetchall()
    for row in result_set:
        vodid = row[0]
        title = row[1]
        author = row[2]
        prev_url = row[3]
        video_time = row[5]
        VODInfo.append({"vodid" : vodid , "title" : title ,"author" : author ,"prev_url" : prev_url ,"video_time" : video_time})
    body = json.dumps(VODInfo)
    return Response(content_type='application/json; charset=utf-8', body=body)


@app.route('/api/v1.0/getpopularVOD', methods=['GET'])
def get_vod_info2():
    VODInfo = []
    db = MySQLdb.connect(host="140.114.77.126", user="hsnl", passwd="hsnl33564", db="twitchhl",charset='utf8')
    cursor = db.cursor()
    command = "SELECT * FROM `videoinfo` ORDER BY clickcount DESC LIMIT 6"
    cursor.execute(command)
    db.commit()
    result_set = cursor.fetchall()
    for row in result_set:
        vodid = row[0]
        title = row[1]
        author = row[2]
        prev_url = row[3]
        video_time = row[5]
        VODInfo.append({"vodid" : vodid , "title" : title ,"author" : author ,"prev_url" : prev_url ,"video_time" : video_time})
    body = json.dumps(VODInfo)
    return Response(content_type='application/json; charset=utf-8', body=body)


@app.route('/api/v1.0/updateClick/<string:id>', methods=['GET'])
def click_update(id):
    db = MySQLdb.connect(host="140.114.77.126", user="hsnl", passwd="hsnl33564", db="twitchhl",charset='utf8')
    cursor = db.cursor()
    command = "UPDATE `videoinfo` SET clickcount = clickcount+1 WHERE id =" + id
    cursor.execute(command)
    db.commit()
    return Response(content_type='application/json; charset=utf-8', body="OK")

@app.route('/api/v1.0/updateInfo', methods=['GET'])
def video_Info_update():
    VODid = []
    db = MySQLdb.connect(host="140.114.77.126", user="hsnl", passwd="hsnl33564", db="twitchhl",charset='utf8')
    cursor = db.cursor()
    command = "SELECT id FROM `videoinfo`"
    cursor.execute(command)
    db.commit()
    result_set = cursor.fetchall()
    for row in result_set:
        cursor2 = db.cursor()
        url = "https://api.twitch.tv/kraken/videos/v"+str(row[0])
        VODBody = requests.get(url, headers = { 'Client-ID':'jwwt96ysrnu4kc0cl4v65gecxqxr9iw' }).json()
        VODInfo = { "title" : VODBody['title'],
        "date" : VODBody['recorded_at'],
        "preview_url" : VODBody['preview'] ,
        "author" : VODBody['channel']['display_name'] + "(" + VODBody['channel']['name'] +")"
        }
        command2 = "UPDATE `videoinfo` SET title = \""+VODInfo['title']+"\" , preview_url = \""+VODInfo['preview_url']+"\" WHERE id =" + str(row[0])
        cursor2.execute(command2)
        db.commit()
    return Response(content_type='application/json; charset=utf-8', body="OK")

if __name__ == "__main__":
    app.run(host='0.0.0.0',threaded=True, port=4000)
