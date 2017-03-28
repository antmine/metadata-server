import sys
import json
import serverReception
import LogQueue
import sqlThread

from threading import Thread

configFilePath =  None;

if (os.envrion['CONFIG_FILE'])
	configFilePath = os.envrion['CONFIG_FILE']
else
	configFilePath = './conf/config.json'

with open(configFilePath, 'r') as f:
	configData = json.load(f)

if __name__ == '__main__':
    ### bdd Thread ###
    sql_thread = sqlThread.sqlThread()
    sql_thread.start()
    ### serverReception Thread ###
    serverReception_thread = serverReception.serverReception()
    serverReception_thread.start()
