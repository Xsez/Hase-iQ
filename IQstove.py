#communication class for Hase iQ stoves
import asyncio
import base64
import datetime
import time
import websockets

class IQstove:
    class Commands:
        state = [
                    "appPhase",         #current phase. enum: 0=idle 1=heating up 2=burning 3=add wood 4=dont add wood 
                    "appT",             #temperature in celsius
                    "appAufheiz",       #heating percentage - on first heating it seems to correlate with target temperature 470c. doesnt seem to only correlate with temperature afterwards
                    "appP",             #performance in percent
                    "appNach",          #??? always zero?
                    "appErr",           #error state
                    ]      

        statistics = [
                    "appPTx",           #length of availabe 1min performance history - should start at 0 on first heatup, goes to max 60
                    "appP30Tx",         #length of availabe heating cycle performance - if 30 cycles are reached it should stay at 30
                    "appPT[0;59]",      #performance history of last 60min
                    "appP30T[0;29]",    #performance history of last 30 cycles
                    "appIQDarst",       #?intensity of iq logo during stop adding wood dialog in app?
                    ]

        info = [
                    "_oemdev",          #stove model - enum: 6=sila (plus)
                    "_oemver",          #controller version
                    "_wversion",        #wifi version
                    "_oemser",          #serialnumber
                    "_ledBri",          #led brightness
                    ]   

        all = []
        all.extend(state)
        all.extend(statistics)
        all.extend(info)


    def __init__(self, ip):
        self.values = {}
        self.ip = ip
        self.model = self.getValue("_oemdev")
        self.serial = self.getValue("_oemser")
        self.controllerVersion = self.getValue("_oemver")
        self.wifiVersion = self.getValue("_wversion")

    def createB64CommandString(self, command):
        commandString = "_req="+command
        commandB64Bytes = base64.b64encode(commandString.encode("ascii"))
        commandB64String = commandB64Bytes.decode("ascii") + "\r"
        return commandB64String
    
    # drive the client connection
    async def sendRequest(self, command):
        # open a connection to the server
        async with websockets.connect(f"ws://{self.ip}:8080") as websocket:
            #print('Connected to server')

            # send a message to server
            try:
                await websocket.send(self.createB64CommandString(command))
            except Exception as e:
                print (f"Error on send: {e}")

            # read message from server
            try:
                message = await websocket.recv()
                messageb64 = base64.b64decode(message).decode('ascii')
                # report result
                #print(f"Received: {messageb64}")
                for command in self.Commands.all:
                    if (messageb64.find(command+"=")>=0):
                        self.values[command] = messageb64.removeprefix(command+"=")

                        return self.values[command]
            except Exception as e:
                print (f"Error on receive: {e}")

        #print('Disconnected')

    def getValue(self, command):
        return asyncio.run(self.sendRequest(command))
    
    @property
    def temperature(self):
        return self.getValue("appT") 
    
    @property
    def performance(self):
        return self.getValue("appP") 
    
    @property
    def phase(self):
        return self.getValue("appPhase") 
    
    @property
    def heatingPercentage(self):
        return self.getValue("appAufheiz") 
    
    @property
    def error(self):
        return self.getValue("appErr") 


# example usage
stove = IQstove("192.168.1.158")

print(f"Stove {stove.serial} connected. Controllver version: {stove.controllerVersion} Wifi version: {stove.wifiVersion} {stove.model}")
print(f"Temperature: {stove.temperature}°C currently in {stove.phase} phase")

for command in stove.Commands.statistics:    
        print(f"{command}: {stove.getValue(command)}")

while True:
    for command in stove.Commands.state:    
        stove.getValue(command)
    print(datetime.datetime.now(), stove.values)
    time.sleep(5)

