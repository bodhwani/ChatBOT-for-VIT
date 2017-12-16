import pandas as pd,os
import nltk,pickle,websocket,time,thread,json,requests,logging
os.chdir(os.getcwd())
logging.basicConfig()
url="ws://54.245.5.208/"
botname="mad_bot"
key="OGU2M2NhODQtYTY2Zi00YWE1LWE5NjAtM2RjZjJlYjg4YWVjNTRkMGQwY2QtM2Fi"
class apiextraction():
	def __init__(self,filename="",load=""):
		if load!="":
			self.featuresets=self.load()
		else:
			self.filename=filename
			self.training_data=self.process_dataset()
			self.featuresets = [(self.process_sentence(n), intent) for (n, intent) in self.training_data]
			self.featuresets = [ (n, intent) for (n, intent) in self.featuresets if n]
		self.classifier= nltk.NaiveBayesClassifier.train(self.featuresets)
	def save(self):
		pickle.dump(self.featuresets, open( "featuresets", "wb" ) )
	def load(self):
		return pickle.load( open( "featuresets", "rb" ) )
	def process_dataset(self):
		df = pd.read_csv(self.filename)
		training_data = []
		for i in range(len(df)):
			training_data.append((df['Text'][i],df['Category'][i]))
		return training_data
	def bag_of_words(self,words):
		return dict([(word, True) for word in words])
	def process_sentence(self,x):
		words = nltk.tokenize.word_tokenize(x.lower()) 
		postag= nltk.pos_tag(words)
		stopwords = nltk.corpus.stopwords.words('english')
		lemmatizer = nltk.WordNetLemmatizer()
		processedwords=[]	
		for w in postag:
		    if "VB" in w[1]:
		        processedwords.append(lemmatizer.lemmatize(w[0].lower(),'v'))
		    else:
		        processedwords.append(lemmatizer.lemmatize(w[0],'n').lower())
		l=[]
		for w in processedwords:
		    if w.lower()=="not":
		        l.append(w)
		    elif w not in stopwords:
		        if (len(w)>2):
		            l.append(w)
		return self.bag_of_words(l)
	def score(self,input_sent):		
		input_sent = input_sent.lower()
		dist = self.classifier.prob_classify(self.process_sentence(input_sent))
		temp=[]
		for label in dist.samples():
		    temp.append((label, dist.prob(label)))
		return temp
	def intent(self,input_sent):
		dist = self.classifier.classify(self.process_sentence(input_sent))
		prob = self.score(input_sent)
		prob = sorted(prob,key=lambda x:(-x[1],x[0]))
		if(prob[0][1]<0.5):
			return  "fallback"
		else:
			return dist
class bot():
	def __init__(self,botname,key,url):
		self.botname=botname
		self.key=key
		self.url=url
		self.var1=apiextraction("dataset.csv")		
		print("Algorithm Trained.")
		self.var1.save()
		self.ws = websocket.WebSocketApp(self.url,on_message = self.on_message,on_error = self.on_error,on_close = self.on_close,on_open=self.on_open)
		print("Bot Running")
		self.ws.run_forever()
	def decodemsg(self,msgid):
		r=requests.session()
		r.headers["Content-Type"]="application/json; charset=utf-8"
		r.headers["Authorization"]="Bearer " + self.key
		response=r.get("https://api.ciscospark.com/v1/messages/"+msgid)
		response=response.json()
		text=response["text"].encode('utf-8')		
		sender=response["personId"].encode('utf-8')
		roomid=response["roomId"].encode('utf-8')		
		return [text,sender,roomid]
	
	def postmsg(self,room,text):
		p = requests.session()
		p.headers["Content-Type"]="application/json; charset=utf-8"
		p.headers["Authorization"]="Bearer "+self.key
		payload={"text":str(text),"markdown":str(text),"roomId":str(room)}
		res=p.post("https://api.ciscospark.com/v1/messages/",json=payload)
	
	def on_error(self,ws,error):
		print(error)
	
	def on_close(self,ws):
		print("Bot Stopped")
		
	def on_message(self,ws,message):
		try:
			data=json.loads(message)
		except:
			data=""
			botname=""
			sender=""
		finally:
			if data:
				botname=data["name"]
				sender=data["data"]["personEmail"]
				msgid=data["data"]["id"]
				decoded=self.decodemsg(msgid)
				print("Message: "+str(decoded[0])+ "\nSender:  " +str(decoded[1])+"\nRoom:   " +str(decoded[2]))
				self.postmsg(decoded[2],self.var1.intent(decoded[0]))
				
	def on_open(self,ws):
		def run(*args):
			ws.send("subscribe:"+self.botname)
			while(1):
				time.sleep(30)
				ws.send("")
			ws.close()
			print("thread terminating...")
		thread.start_new_thread(run, ())
if __name__ == "__main__":
	var2=bot(botname,key,url)
