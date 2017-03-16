import sys
import json
import serverReception
import LogQueue

from threading import Thread

with open('./conf/config.json', 'r') as f:
	configData = json.load(f)

queue = LogQueue.LogQueue(configData['queueSize'])

if __name__ == '__main__':
    ### serverReception Thread ###
    serverReception_thread = serverReception.serverReception()
    serverReception_thread.start()
