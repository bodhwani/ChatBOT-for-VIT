import websocket,time,thread,json,requests,logging
logging.basicConfig()

class bot():
	def __init__(self,botname,key,url):
		self.botname=botname
		self.key=key
		self.url=url
		self.ws = websocket.WebSocketApp(self.url,on_message = self.on_message,on_error = self.on_error,on_close = self.on_close,on_open=self.on_open)
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
		payload={"text":str(text),"markdown":str("yo"),"roomId":str(room)}
		res=p.post("https://api.ciscospark.com/v1/messages/",json=payload)
	
	def on_error(self,ws,error):
		print(error)
	
	def on_close(self,ws):
		print("### Closed ###")
		
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
				self.postmsg(decoded[2],decoded[0])
				
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
    var=bot(botname,key,url)
       
