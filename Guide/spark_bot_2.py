import websocket
import time
import thread
import json
import requests
# botname="bot_a_thon_1"
# key="ZDA0YzVmN2QtM2RmMi00YjEyLWJiYTYtYjJhN2RiZDI1OWFiZWIyYTQwM2UtY2U4"


# botname="temp_bot0719"
# key="ZmQ4M2M1OTctYTVhOS00NDc3LTgzZWItNmMzOTJkYzI5ZjdkYzJjMDU0YTgtZjJh"

botname="temp_bot0719"
# key="NjhjYTVlMjEtMjRmNi00NDdlLThmZmYtM2YyYWExNDliOGRhZWM3Y2Q1ZDgtYTdh"
key = "NTlkMmQ1ZDUtODYwMi00ZDFkLWEzMmYtZGNiMTNkYjIxMzI2ZjQwN2U3NDItMTQy"



def decodemsg(msgid,key):
    print "inside decodemsg"
    r = requests.session()
    r.headers["Content-Type"]="application/json; charset=utf-8"
    r.headers["Authorization"]="Bearer " + key
    response=r.get("https://api.ciscospark.com/v1/messages/"+msgid)
    response=json.loads(response.text)
    text=response["text"]
    print "text is",text
    print "\n\n"
    print "msge id is",msgid
    sender=response["personId"]
    roomid=response["roomId"]
    return [text,sender,roomid,key]

def postmsg(room,text,key):
    p = requests.session()
    p.headers["Content-Type"]="application/json; charset=utf-8"
    p.headers["Authorization"]="Bearer "+key
    payload={"text":str(text),"markdown":str(text),"roomId":str(room)}
    # print "Here is the payload",payload
    res=p.post("https://api.ciscospark.com/v1/messages/",json=payload)

def on_message(ws,message):
    print "inside message"
    try:
        data=json.loads(message)
        print "data is",data
    except:
        data=""
        botname=""
        sender=""
    if data:
        botname=data["name"]
        sender=data["data"]["personEmail"]
        if(sender == "vinitbodhwani123@gmail.com"):        
            msgid=data["data"]["id"]
            decoded=decodemsg(msgid,key)
            print(decoded)
            postmsg(decoded[2],decoded[0],key)
    else:
        print "no data"

def on_error(ws, error):
    print "error is",error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        print "in run..."
        ws.send("subscribe:"+botname)
        print "hello"
        while(1>0):
            time.sleep(30)
            ws.send("")
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())



if __name__ == "__main__":
    # ws = websocket.WebSocketApp("ws://54.245.5.208/",on_message = on_message,on_error = on_error,on_close = on_close)
    # ws = websocket.WebSocketApp("ws://echo.websocket.org:80",on_message = on_message,on_error = on_error,on_close = on_close)
    # ws.on_open = on_open
    # ws.run_forever()

    prev=""
    while(True):
        rg = requests.get("https://nlpbot.herokuapp.com/output")
        # print "rg-text is",rg.text
        # print "prev is ",prev
        if(rg.text!=prev):
            # print ""
            # print "Processing message is", rg.text
            on_message("ws",rg.text)
            prev=rg.text

        # time.sleep(30)
        if(rg.text=="STOP"):
            break 


#room id(nlpbot) = Y2lzY29zcGFyazovL3VzL1JPT00vNWVlYzE1MDAtZDZmMi0xMWU4LTkxMzYtZTVkZTBkZTg5NjFk
