import websocket
import time
import thread

botname="temp_bot0719"

def on_message(ws,message):
    print(message)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        print "running..."
        ws.send("subscribe:"+botname)
        print "running 2"
        while(1>0):
            time.sleep(30)
            ws.send("")
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())



if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://echo.websocket.org:80",on_message = on_message,on_error = on_error,on_close = on_close)
    # ws = websocket.WebSocketApp("ws://54.245.5.208/",on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
