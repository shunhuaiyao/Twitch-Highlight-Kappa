import rechat
import time
import requests
from sklearn import svm
from sklearn import ensemble
from sklearn.naive_bayes import GaussianNB
#import restful_api
MIN_HIGHLIGHTS = 5
N_ESTIMATORS = 50
#ensemble.RandomForestClassifier(n_estimators=N_ESTIMATORS)  svm.SVC()  GaussianNB()
clf = ensemble.RandomForestClassifier(n_estimators=N_ESTIMATORS)
output_type = "RF"

def main(test_VoD,  mode):
	TIME_INTERVAL = rechat.get_frame_secs()
	#Training
	TRAINING_VOD = '108244967'

	if(mode == 'reTrain'):
		url = 'https://rechat.twitch.tv/rechat-messages'
		url1 = url + '?' + 'start=0&video_id=v' +  test_VoD
		re = requests.get(url1).json()
		detail = re['errors'][0]['detail'].split(' ')
		start = int(detail[4])
	elif(mode =='newVoD'):
		start = rechat.getChat(test_VoD, 'v')
	
	highlight_time = rechat.get_highlight_time('train_highlight_time.txt')
	_time, train_data, train_labels = rechat.extract_features(TRAINING_VOD, highlight_time)
	_time, data = rechat.extract_features(test_VoD, None)
	N = 1
	best_result = []
	while(True):
		testing_result = []
		#clf = ensemble.RandomForestClassifier(n_estimators=N_ESTIMATORS)
		rechat.train_model(clf, train_data, train_labels)
		print('------------Testing result: '+str(N)+'--------------')
		result = clf.predict(data)
		stack_frames = []
		for i in range(len(result)):
			if(result[i]==False):
				continue
			#print("results??")
			t = int(_time[i])
			num_of_stack_frames = len(stack_frames)
			if(num_of_stack_frames>0):
				last_frame = stack_frames[-1]
				if((t-last_frame)<=2*TIME_INTERVAL):
					stack_frames.append(t)
				else:
					#if(len(stack_frames)>3):
					if(num_of_stack_frames>3 and num_of_stack_frames<=12):
						#highlight_start = time.strftime('%H:%M:%S',  time.gmtime(stack_frames[0]-start-TIME_INTERVAL))
						#highlight_end = time.strftime('%H:%M:%S',  time.gmtime(stack_frames[-1]+TIME_INTERVAL-start+15))
						highlight_start = str(stack_frames[0]-start-2*TIME_INTERVAL)
						highlight_end = str(stack_frames[-1]-start)
						h = (highlight_start + ' ' + highlight_end)
						testing_result.append(h)
						highlight_start = time.strftime('%H:%M:%S',  time.gmtime(int(highlight_start)))
						highlight_end = time.strftime('%H:%M:%S',  time.gmtime(int(highlight_end)))
						print('Start time: '+ highlight_start)
						print('End time: '+ highlight_end)
						print('--------------------')
					stack_frames = []
					stack_frames.append(t)
			else:
				stack_frames.append(t)
		#if(len(stack_frames)>3):
		if(len(stack_frames)>3 and num_of_stack_frames<=12):
			#highlight_start = time.strftime('%H:%M:%S',  time.gmtime(stack_frames[0]-start-TIME_INTERVAL))
			#highlight_end = time.strftime('%H:%M:%S',  time.gmtime(stack_frames[-1]+TIME_INTERVAL-start+15))
			highlight_start = str(stack_frames[0]-start-2*TIME_INTERVAL)
			highlight_end = str(stack_frames[-1]-start)
			h = (highlight_start + ' ' + highlight_end)
			testing_result.append(h)
			highlight_start = time.strftime('%H:%M:%S',  time.gmtime(int(highlight_start)))
			highlight_end = time.strftime('%H:%M:%S',  time.gmtime(int(highlight_end)))
			print('Start time: '+ highlight_start)
			print('End time: '+ highlight_end)
			print('--------------------')

				#highlight = int(_time[i])-start
				#highlight = time.strftime('%H:%M:%S',  time.gmtime(highlight))
				#print(highlight)
		N = N + 1
		if(len(testing_result)>len(best_result)):
			# and len(testing_result)<15
			best_result = testing_result
		if(len(best_result)>MIN_HIGHLIGHTS):
			break
		elif(N>200):
			break

	#fw = open('./output_highlight_'+test_VoD+'_'+output_type+'.txt', 'w', encoding='utf-8')
	fw = open('./output_highlight_'+test_VoD+'.txt', 'w', encoding='utf-8')
	for line in best_result:
		fw.write(line+'\n')
	fw.close()
	#restful_api.set_vod_info(test_VoD)
	if(mode == 'newVOD'):
		url = "http://localhost:4000/api/v1.0/setVODInfo/"+test_VoD
		requests.get(url)


test_VoD_list = [('108244967',1482050827), ('109912038', 1482748606),('109562655', 1482581989),('103451043', 1480155698), ('102642788',1479805879)]
'''
for vod in test_VoD_list:
	test_VoD, start = vod
	main(test_VoD)
'''
