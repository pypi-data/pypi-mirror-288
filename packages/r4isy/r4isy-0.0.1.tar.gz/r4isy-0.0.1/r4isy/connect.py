import sys
import time
import loadwave

def main():
    arg = sys.argv[1]
    if(arg == "r4isy-1"):
        HOST = "245.141.151.141"
        connectserver(arg, HOST)
    
    else:
        print("This server is invalid.")
        exit()
        """elif(arg == "r4isy-2"):
        HOST = "20.250.2.200"
        print()"""
    
def connectserver(server, servername ="r4isy-1"):
    print("Connecting to the server. - " + servername)
    connectserverld()

@loadwave.process
def connectserverld():
    time.sleep(3.5)
    print("A connection error occurred. The server is down or under maintenance. Please try again later.")