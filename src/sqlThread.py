#!/usr/bin/env python3.5

import json
import os
import sys
import threading
import LogQueue
import time
import run as main

from flask import Flask
from flaskext.mysql import MySQL
#sqlalchemy imports
from sqlalchemy import create_engine, MetaData, Table

import serverReception

with open('./conf/' + os.getenv('CONFIG_FILE', 'config') + '.json', 'r') as f:
	configData = json.load(f)


class sqlThread(threading.Thread):

	engine = None
	metadata = None
	miner_event = None

	app = Flask(__name__)

	def __init__(self):
		self.initSql()
		threading.Thread.__init__(self)

	def checkEvent(self, json):
		try:
			con = self.engine.connect()
			if 'isTabActive' in json:
				con.execute(self.miner_event.insert(), ID_MINER=json['id'], URL=json['url'], TAB_ACTIVE=json['isTabActive'])
			elif 'isDisconnected' in json:
				con.execute(self.miner_event.insert(), ID_MINER=json['id'], URL=json['url'], DISCONNECTED=json['isDisconnected'])
			elif 'isOnBattery' in json:
				con.execute(self.miner_event.insert(), ID_MINER=json['id'], URL=json['url'], ON_BATTERY=json['isOnBattery'])
		except:
			print ("Unexpected error:", sys.exc_info()[1])

	def run(self):
		print('run')
		sys.stdout.flush()
		while True:
			print('acquire')
			serverReception.condition.acquire()
			if len(LogQueue.LogQueue.Instance().queue) > 0:
				print('message !!!')
				jsonData = LogQueue.LogQueue.Instance().getLog()
				serverReception.condition.release()
				self.checkEvent(jsonData)
			else:
				print('wait !!!')
				serverReception.condition.wait()
				print('end wait !!!')

	def initSql(self):
			#create the connection with mysql db
			self.engine = create_engine(configData["SQL"]["type"]+configData["SQL"]["user"]+':'+configData["SQL"]["password"]+'@' + configData["SQL"]["url"]+'/'+configData["SQL"]["databaseName"], convert_unicode=True)
			self.metadata = MetaData(bind = self.engine)

			#loads all the MINER_EVENT table details
			self.miner_event = Table('MINER_EVENT', self.metadata, autoload=True)
