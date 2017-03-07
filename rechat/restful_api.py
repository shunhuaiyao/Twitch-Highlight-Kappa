from flask import Flask
from flask import render_template
from webob import Response
import _thread
import os
import json
import requests
import main
import WordCloud
from flask_cors import CORS

trainingVOD = []

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


app = Flask(__name__)
CORS(app)
@app.route('/', methods=['GET'])

@app.route('/api/v1.0/vodTitle/<string:id>', methods=['GET'])
def get_vod_title(id):
	url = "https://api.twitch.tv/kraken/videos/v"+id
	VODInfo = requests.get(url, headers = { 'Client-ID':'jwwt96ysrnu4kc0cl4v65gecxqxr9iw' }).json()
	VODTitle = []
	#print(VODInfo['title'])
	VODTitle.append({"title" : VODInfo['title'].encode('utf-8')})
	body = json.dumps(VODTitle)
	return Response(content_type='application/json; charset=utf-8', body=body)


@app.route('/api/v1.0/vodHighlight/<string:id>', methods=['GET'])
def get_vod_highlight(id):

	HL_VODs = {"status":"false","videos":[]}

	if os.path.isfile("./output_highlight_"+id+".txt") :
		f = open("./output_highlight_"+id+".txt", 'r')
		for line in f.readlines():
			HL_start_end = line.split()
			HL_VODs['videos'].append({"start" : HL_start_end[0] , "end" : HL_start_end[1]})
		HL_VODs['status'] = "true"
		if id in trainingVOD:
			trainingVOD.remove(id)
		body = json.dumps(HL_VODs)
		return Response(content_type='application/json; charset=utf-8', body=body)

	else:
		#print("not exsit")
		if id not in trainingVOD :
			trainingVOD.append(id)
			#global thread
			#thread = Thread(target = main.main(id))
			_thread.start_new_thread(main.main, (id, 'newVoD', ))
			#main.main(id)
			if os.path.isfile("./output_highlight_"+id+".txt") :
				f = open("./output_highlight_"+id+".txt", 'r')
				for line in f.readlines():
					HL_start_end = line.split()
					HL_VODs['videos'].append({"start" : HL_start_end[0] , "end" : HL_start_end[1]})
				trainingVOD.remove(id)
				HL_VODs['status'] = "true"
			body = json.dumps(HL_VODs)
			return Response(content_type='application/json; charset=utf-8', body=body)
		else :
			body = json.dumps(HL_VODs)
			return Response(content_type='application/json; charset=utf-8', body=body)
	

@app.route('/api/v1.0/vodKeyword/<string:id>', methods=['GET'])
def get_vod_Keyword(id):
	
	kw_VODs = {"status": "false", "content": []}

	if os.path.isfile("./data/"+id+"_keyword.txt") :
		f = open("./data/"+id+"_keyword.txt", 'r', encoding='utf-8-sig')
		kw_VODs['content'] = f.readlines()[0]
		kw_VODs['status'] = "true"
		#print(kw_VODs['content'])
	else:
		if os.path.isfile("./data/VoD_"+id+".txt") :
			WordCloud.PrintTFIDFTotxt(id)
		if os.path.isfile("./data/"+id+"_keyword.txt") :
			f = open("./data/"+id+"_keyword.txt", 'r', encoding='utf-8-sig')
			kw_VODs['content'] = f.readlines()[0]
			kw_VODs['status'] = "true"

	body = json.dumps(kw_VODs)
	return Response(content_type='application/json; charset=utf-8', body=body)


@app.route('/api/v1.0/vodHighlight/<string:id>/train/<string:ifTrain>', methods=['GET'])
def train_vod_highlight(id, ifTrain):
	
	_thread.start_new_thread(main.main, (id, 'reTrain', ))

	body = "ok"
	return Response(content_type='application/json; charset=utf-8', body=body)

if __name__ == "__main__":
    app.run(host='0.0.0.0',threaded=True)
