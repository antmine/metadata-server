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
import serverReception

with open('./conf/' + os.getenv('CONFIG_FILE', 'config') + '.json', 'r') as f:
	configData = json.load(f)

class sqlThread(threading.Thread):

	cursor = None
	connection = None
	app = Flask(__name__)

	def __init__(self):
		self.initSql()
		threading.Thread.__init__(self)

	def checkEvent(self, json):
		if 'isTabActive' in json:
			sqlRequest = 'INSERT INTO MINER_EVENT (ID_MINER, URL, TAB_ACTIVE) \
						  VALUES (' + str(json['id']) + ' , \'' + json['url'] + '\', ' + str(int(json['isTabActive'])) + ');'
		elif 'isDisconnected' in json:
			sqlRequest = 'INSERT INTO MINER_EVENT (ID_MINER, URL, DISCONNECTED) \
						VALUES (' + str(json['id']) + ' , \'' + json['url'] + '\', ' + str(int(json['isDisconnected'])) + ');'
		elif 'isOnBattery' in json:
			sqlRequest = 'INSERT INTO MINER_EVENT (ID_MINER, URL, ON_BATTERY) \
						VALUES (' + str(json['id']) + ' , \'' + json['url'] + '\', ' + str(int(json['isOnBattery'])) + ');'
		else:
			sqlRequest = ''

		try:
			self.cursor.execute(sqlRequest)
			self.connection.commit()
		except:
			print ("Unexpected error:", sys.exc_info()[1])

	def run(self):
		sys.stdout.flush()
		while True:
			serverReception.condition.acquire()
			if len(LogQueue.LogQueue.Instance().queue) > 0:
				jsonData = LogQueue.LogQueue.Instance().getLog()
				serverReception.condition.release()
				self.checkEvent(jsonData)
				# self.process_data()
			else:
				serverReception.condition.wait()

	def initSql(self):
		mysql = MySQL()
		self.app.config['MYSQL_DATABASE_USER'] = configData["mysql"]["user"]
		self.app.config['MYSQL_DATABASE_PASSWORD'] = configData["mysql"]["password"]
		self.app.config['MYSQL_DATABASE_HOST'] = configData["mysql"]["url"]
		self.app.config['MYSQL_DATABASE_DB'] = configData["mysql"]["database"]
		mysql.init_app(self.app)
		self.connection = mysql.connect()
		self.cursor = self.connection.cursor()

	def process_data(self):
		sql = "SELECT * from IS_DISCONNECTED;"
		self.cursor.execute(sql)
		data = self.cursor.fetchall()
		for values in data:
			sys.stdout.write("events disconnected: " + str(values) + '\n')
			sys.stdout.flush()
		sql = "SELECT * from IS_BATTERY;"
		self.cursor.execute(sql)
		data = self.cursor.fetchall()
		for values in data:
			sys.stdout.write("events battery: " + str(values) + '\n')
			sys.stdout.flush()
		sql = "SELECT * from IS_TAB_ACTIV;"
		self.cursor.execute(sql)
		data = self.cursor.fetchall()
		for values in data:
			sys.stdout.write("events tabActiv: " + str(values) + '\n')
			sys.stdout.flush()
