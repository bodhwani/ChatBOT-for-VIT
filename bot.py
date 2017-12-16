import websocket,time,thread,json,requests,os

botname="mad_bot" #bot_name
key="MjMwOTZkNjQtYjdkYi00MDUyLThlNDktMTg0MzZkM2NjMzg3Y2Y3NDFjNzEtOWE3" #refrence code

class bot():
	def init(self,botname,access_code,url="ws://54.245.5.208/"):
		self.botname=botname
		self.access_code=access_code
		self.url=url
    ws = websocket.WebSocketApp(self.url,on_message = self.on_message,on_error = self.on_error,on_close = self.on_close)
    ws.on_open = on_open
    ws.run_forever()
    
	def on_message(ws,message):
		try:
	    data=json.loads(message)
	    #print(data)
		except:			
		  data=""
	    botname=""
	    sender=""
		if data:		
	    botname=data["name"]
	    sender=data["data"]["personEmail"]
	    msgid=data["data"]["id"]
	    decoded=self.decodemsg(msgid)
	    print(decoded)
	    self.postmsg(decoded[2],decoded[0],key)

	def on_error(ws, error):
		print(error)

	def on_close(ws):
		print "### closed ###"

	def on_open(ws):
		def run(*args):			
	    ws.send("subscribe:"+botname)
	    while(1>0):
        time.sleep(30)
        ws.send("")
	    ws.close()
	    print("thread terminating...")
	thread.start_new_thread(run, ())

	def decodemsg(msgid):
		r = requests.session()
		r.headers["Content-Type"]="application/json; charset=utf-8"
		r.headers["Authorization"]="Bearer " + self.key
		response=r.get("https://api.ciscospark.com/v1/messages/"+msgid)
		response=json.loads(response.text)
		text=response["text"]
		sender=response["personId"]
		roomid=response["roomId"]
		return [text,sender,roomid]

	def postmsg(room,text,key):
		p = requests.session()
		p.headers["Content-Type"]="application/json; charset=utf-8"
		p.headers["Authorization"]="Bearer "+key
		payload={"text":str(text),"markdown":str("yo"),"roomId":str(room)}
		res=p.post("https://api.ciscospark.com/v1/messages/",json=payload)




if __name__ == "__main__":
	var=bot(botname,key)

