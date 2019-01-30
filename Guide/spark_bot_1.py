import websocket
import time
import thread
import json
import requests

# botname="bot_a_thon_1"
# key="ZDA0YzVmN2QtM2RmMi00YjEyLWJiYTYtYjJhN2RiZDI1OWFiZWIyYTQwM2UtY2U4"




botname="temp_bot0719"
key = "NTlkMmQ1ZDUtODYwMi00ZDFkLWEzMmYtZGNiMTNkYjIxMzI2ZjQwN2U3NDItMTQy"

def decodemsg(msgid,key):
    print "decoding"
    r = requests.session()
    r.headers["Content-Type"]="application/json; charset=utf-8"
    r.headers["Authorization"]="Bearer " + key
    response=r.get("https://api.ciscospark.com/v1/messages/"+msgid)
    response=json.loads(response.text)
    text=response["text"]
    sender=response["personId"]
    roomid=response["roomId"]
    return [text,sender,roomid]

def on_message(ws,message):
    print "Message is ",message
    try:
        data=rg.text
        #print(data)
    except:
        data=""
        botname=""
        sender=""
    if data:
        # print "data is ",data
        botname="temp_bot0719"
        sender="vinitbodhwani123@gmail.com"
        msgid="Y2lzY29zcGFyazovL3VzL01FU1NBR0UvM2ZhNTBjNjAtMzI2Zi0xMWU4LWExMjAtNGJkN2Q2MmIyZTBm"
        decoded=decodemsg(msgid,key)
        print(decoded)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "entered in open"
    def run(*args):
        ws.send("subscribe:"+botname)
        while(1>0):
            print "chal rha hai"
            time.sleep(30)
            ws.send("hihihihihi")
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())



if __name__ == "__main__":
    # ws = websocket.WebSocketApp("ws://echo.websocket.org:80",on_message = on_message,on_error = on_error,on_close = on_close)
    # # ws = websocket.WebSocketApp("ws://54.245.5.208/",on_message = on_message,on_error = on_error,on_close = on_close)
    # ws.on_open = on_open
    # ws.run_forever()


    prev=""
    while(True):
        rg = requests.get("https://nlpbot.herokuapp.com/output")
        if(rg.text!=prev):
            print ""
            print "Processing message is", rg.text
            on_message("ws",rg.text)
            prev=rg.text
        if(rg.text=="STOP"):
            break  
