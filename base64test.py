import base64

def createB64CommandString(command):
    commandString = "_req="+command
    commandB64Bytes = base64.b64encode(commandString.encode("ascii"))
    commandB64String = commandB64Bytes.decode("ascii") + "\r"
    return commandB64String

commands = ["appPhase",
            "appT",
            "appAufheiz",
            "appErr",
            "_oemdev",
            "_oemver",
            "_wversion",
            "appPTx",
            "appP30Tx",
            "appPT[0;14]"]

print(createB64CommandString(commands[0]))