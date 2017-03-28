import sys
import os
import json
import serverReception
import LogQueue
import sqlThread

from threading import Thread

with open('./conf/' + os.getenv('CONFIG_FILE', 'config') + '.json', 'r') as f:
	configData = json.load(f)

if __name__ == '__main__':
    ### bdd Thread ###
    sql_thread = sqlThread.sqlThread()
    sql_thread.start()
    ### serverReception Thread ###
    serverReception_thread = serverReception.serverReception()
    serverReception_thread.start()
