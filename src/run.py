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
			### bdd Thread ###
			sql_thread = sqlThread.sqlThread()
			sql_thread.daemon = True
			sql_thread.start()
			### serverReception Thread ###
			serverReception_thread = serverReception.serverReception()
			serverReception_thread.daemon = True
			serverReception_thread.start()
		except KeyboardInterrupt:
			sys.exit(1)
