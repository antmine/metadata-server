#!/usr/bin/env python3.5

import json
import os
import sys
import threading
import LogQueue
import time
import run as main

from urllib.parse import urlparse
from flask import Flask
# from flask.ext.mysql import MySQL
#sqlalchemy imports
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select

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
			conApp = self.engineApplication.connect()
			conAdm = self.engineAdministration.connect()
			if 'newId' in json:
				url = urlparse(json['url'])
				conApp.execute(self.miner.insert(), ID_MINER=json['newId'], POWER_ESTIMATION=0)
				result = conAdm.execute(select([self.website.c.ID_WEBSITE]).where(self.website.c.URL == url.netloc))
				row = result.fetchone()
				conApp.execute(self.miner_website.insert(), ID_MINER=json['newId'], ID_WEBSITE=row[self.website.c.ID_WEBSITE])
			elif 'scriptState' in json:
				if json['scriptState'] == 'stop':
					conApp.execute(self.miner_event.insert(), ID_MINER=json['id'], URL=json['url'], IS_MINING=False)
				else:
					conApp.execute(self.miner_event.insert(), ID_MINER=json['id'], URL=json['url'], IS_MINING=True)
		except:
			print ("Unexpected error:", sys.exc_info()[1])

	def run(self):
		while True:
			serverReception.condition.acquire()
			if len(LogQueue.LogQueue.Instance().queue) > 0:
				jsonData = LogQueue.LogQueue.Instance().getLog()
				serverReception.condition.release()
				self.checkEvent(jsonData)
			else:
				serverReception.condition.wait()

	def initSql(self):
			#create the connection with mysql db
			self.engineApplication = create_engine(configData["SQL"]["type"]+configData["SQL"]["user"]+':'+configData["SQL"]["password"]+'@' + configData["SQL"]["url"]+'/'+configData["SQL"]["databaseName"], convert_unicode=True)
			self.engineAdministration = create_engine(configData["SQL"]["type"]+configData["SQL"]["user"]+':'+configData["SQL"]["password"]+'@' + configData["SQL"]["url"]+'/ADMINISTRATION', convert_unicode=True)
			self.metadataApplication = MetaData(bind = self.engineApplication)
			self.metadataAdministration = MetaData(bind=self.engineAdministration)

			#loads all the MINER_EVENT & MINER_WEBSITE table details
			self.miner_event = Table('MINER_EVENT', self.metadataApplication, autoload=True)
			self.miner_website = Table('MINER_WEBSITE', self.metadataApplication, autoload=True)
			self.miner = Table('MINER', self.metadataApplication, autoload=True)
			self.website = Table('WEBSITE', self.metadataAdministration, autoload=True)
