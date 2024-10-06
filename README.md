# Hase-iQ
Example communication to a Hase iQ Stove

Communication is unencrypted websocket text. Text payload is ascii encoded base64.

Known Commands:

commandsCurrentState

            "appPhase",         #current phase. enum: 0=idle 1=heating up 2=burning 3=add wood 4=dont add wood 
            "appT",             #temperature in celsius
            "appAufheiz",       #heating percentage - on first heating it seems to correlate with target temperature 475c. doesnt seem to only correlate with temperature afterwards
            "appP",             #performance in percent
            "appNach",          #??? always zero?
            "appErr",           #error state
                 

commandsStatistics

            "appPTx",           #length of availabe 1min performance history - should start at 0 on first heatup, goes to max 60
            "appP30Tx",         #length of availabe heating cycle performance - if 30 cycles are reached it should stay at 30
            "appPT[0;59]",      #performance history of last 60min
            "appP30T[0;29]",    #performance history of last 30 cycles
            "appIQDarst",       #?intensity of iq logo during stop adding wood dialog in app?
            

commandsInfo

            "_oemdev",          #stove model - enum: 6=sila (plus)
            "_oemver",          #controller version
            "_wversion",        #wifi version
            "_oemser",          #serialnumber
            "_ledBri",          #led brightness
             

Example

    Websocket text payload raw: "X3JlcT1hcHBQaGFzZQ==\r"
    Decoded to base64: "_req=appPhase"
    Answer from stove payload text: "YXBwUGhhc2U9NA==\r"
    Decoded to base64: "appPhase=4"
