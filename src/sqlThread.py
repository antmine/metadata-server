#!/usr/bin/env python3.5

import json
import sys
import threading
import LogQueue
import run as main

from flask import Flask
from flaskext.mysql import MySQL

with open('./conf/config.json', 'r') as f:
	configData = json.load(f)

class sqlThread(threading.Thread):

    cursor = None
    connection = None
    app = Flask(__name__)

    def __init__(self):
        self.initSql()
        sys.stdout.write("Sql initialized\n")
        sys.stdout.flush()
        threading.Thread.__init__(self)

    def checkEvent(self, json):
        if 'isDisconnected' in json:
            sqlRequest = 'INSERT INTO IS_DISCONNECTED (ID_USER, VALUE_IS_DISCO) VALUES (\''+json['id']+'\', '+json['isDisconnected']+');'
        elif 'isTabActiv' in json:
            sqlRequest = 'INSERT INTO IS_TAB_ACTIV (ID_USER, VALUE_IS_TAB_ACT) VALUES (\''+json['id']+'\', '+json['isTabActiv']+');'
        else:
            sqlRequest = 'INSERT INTO IS_BATTERY (ID_USER, VALUE_IS_BAT) VALUES (\''+json['id']+'\', '+json['isBattery']+');'
        sys.stdout.write(sqlRequest)
        sys.stdout.flush()
        self.cursor.execute(sqlRequest)
        self.connection.commit()

    def run(self):
        sys.stdout.write("Sql thread is running\n")
        sys.stdout.flush()
        while True:
            if len(LogQueue.LogQueue.Instance().queue) > 0:
                jsonData = LogQueue.LogQueue.Instance().getLog()
                self.checkEvent(jsonData)
                self.process_data()

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
