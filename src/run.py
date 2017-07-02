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
		try:
			sys.stdout.write("server listening port: " + str(configData["port"]) + "\n")
			### bdd Thread ###
			print('1')
			sql_thread = sqlThread.sqlThread()
			print('2')
			sql_thread.daemon = True
			print('3')
			sql_thread.start()
			print('4')
			### serverReception Thread ###
			serverReception_thread = serverReception.serverReception()
			serverReception_thread.daemon = True
			serverReception_thread.start()
		except KeyboardInterrupt:
			sys.exit(1)
