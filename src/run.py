import sys
import json
import serverReception
import LogQueue
import bdd

from threading import Thread

with open('./conf/config.json', 'r') as f:
	configData = json.load(f)

if __name__ == '__main__':
    ### bdd Thread ###
    #sql_thread = bdd.sqlThread()
    #sql_thread.start()
    ### serverReception Thread ###
    serverReception_thread = serverReception.serverReception()
    serverReception_thread.start()
