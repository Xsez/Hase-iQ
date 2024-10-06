import time
import websocket
import threading
import base64
import datetime

commandsCurrentState = [
            "appPhase",         #current phase. enum: 0=idle 1=heating up 2=burning 3=add wood 4=dont add wood 
            "appT",             #temperature in celsius
            "appAufheiz",       #heating percentage - on first heating it seems to correlate with target temperature 475c. doesnt seem to only correlate with temperature afterwards
            "appP",             #performance in percent
            "appNach",          #???
            "appErr",           #error state
            ]      

commandsStatistics = [
            "appPTx",           #length of availabe 1min performance history - should start at 0 on first heatup, goes to max 60
            "appP30Tx",         #length of availabe heating cycle performance - if 30 cycles are reached it should stay at 30
            "appPT[0;59]",      #performance history of last 60min
            "appP30T[0;29]",    #performance history of last 30 cycles
            ]

commandsInfo = [
            "_oemdev",          #stove model - enum: 6=sila
            "_oemver",          #controller version
            "_wversion",        #wifi version
            "_oemser",          #serialnumber
            "appIQDarst",       #???
            "_ledBri",          #led brightness
            ]   

commandsAll = []
commandsAll.extend(commandsCurrentState)
commandsAll.extend(commandsStatistics)
commandsAll.extend(commandsInfo)

values = {}  

def createB64CommandString(command):
    commandString = "_req="+command
    commandB64Bytes = base64.b64encode(commandString.encode("ascii"))
    commandB64String = commandB64Bytes.decode("ascii") + "\r"
    return commandB64String

def pollingThread(ws, commands, interval):
    print(f"Thread started for commands: {commands}. Interval {interval} seconds.")
    while True:
        requestString = ""
        for command in commands:
            requestString = requestString + createB64CommandString(command)
        ws.send_text(requestString)
        print(datetime.datetime.now(), values)
        time.sleep(interval)

def startThread(commands, interval):
    thread = threading.Thread(target=pollingThread, args=(ws, commands, interval))
    thread.daemon = True  # This ensures the thread will close when the main program exits
    thread.start() 


#WebSocket connection
ws_url = "ws://192.168.1.158:8080"
try:
    def on_message(ws, message):
        messageb64 = base64.b64decode(message).decode('ascii')
        #print(f"Received message: {messageb64}")
        for command in commandsAll:
            if (messageb64.find(command+"=")>=0):
                values[command] = messageb64.removeprefix(command+"=")
        
            
    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    def on_close(ws):
        print("WebSocket connection closed")

    def on_open(ws):
        print("WebSocket connection established. Starting periodic threads.")
        startThread(commandsCurrentState, 1)
        startThread(commandsStatistics, 60)
        startThread(commandsInfo, 3600)
        

    def on_ping(ws, message):
        pass
        #print(f"Websocket Ping received: {message}. Sending Pong.")

    # Create a WebSocket connection
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_ping=on_ping,
                                on_open= on_open)
    ws.run_forever()  

except Exception as e:
    print(f"Error establishing WebSocket connection: {e}")







# commandsRaw = ["X3JlcT1hcHBQaGFzZQ==\r",        #_req=appPhase
#             "X3JlcT1hcHBU\r",
#             "X3JlcT1hcHBBdWZoZWl6\r",
#             "X3JlcT1hcHBQaGFzZQ==\r",
#             "X3JlcT1hcHBFcnI=\r",
#             "X3JlcT1fb2VtZGV2\r",
#             "X3JlcT1fb2VtdmVy\r",
#             "X3JlcT1fd3ZlcnNpb24=\r",
#             "X3JlcT1hcHBQVHg=\r",
#             "X3JlcT1hcHBQMzBUeA==\r",
#             "X3JlcT1hcHBQVFswOzE0XQ==\r"]

# def threadCommandsCurrentState(ws, interval=1):
#     print(f"Current State Thread started. Interval {interval} seconds.")
#     while True:
#         for command in commandsCurrentState:
#             time.sleep(0.1)  # Wait for the specified interval before sending the next message
#             ws.send_text(createB64CommandString(command))
#             #print(f"Sent request: {command}")
        
#         print(datetime.datetime.now(), values)
#         time.sleep(interval)

# def threadCommandsStatistics(ws, interval=60):
#     print(f"Statistics Thread started. Interval {interval} seconds.")
#     time.sleep(1)
#     while True:
#         for command in commandsStatistics:
#             time.sleep(0.25)  # Wait for the specified interval before sending the next message
#             ws.send_text(createB64CommandString(command))
#             #print(f"Sent request: {command}")
        
#         #print(datetime.datetime.now(), values)
#         time.sleep(interval)

# def threadCommandsInfo(ws, interval=3600):
#     print(f"Statistics Thread started. Interval {interval} seconds.")
#     time.sleep(2)
#     while True:
#         for command in commandsInfo:
#             time.sleep(0.25)  # Wait for the specified interval before sending the next message
#             ws.send_text(createB64CommandString(command))
#             #print(f"Sent request: {command}")
        
#         #print(datetime.datetime.now(), values)
#         time.sleep(interval)