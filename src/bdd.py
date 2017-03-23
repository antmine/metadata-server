#!/usr/bin/env python3.5

import json
import sys
import threading
import LogQueue
import run as main

from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
#configData = json.loads(json.dumps(main.configData))

with open('./conf/config.json', 'r') as f:
	configData = json.load(f)

class sqlThread(threading.Thread):

    cursor = None

    def __init__(self):
        self.initSql()
        sys.stdout.write("Sql initialized\n")
        sys.stdout.flush()
        threading.Thread.__init__(self)

    def run(self):
        sys.stdout.write("Sql thread is running\n")
        sys.stdout.flush()
        while True:
            if len(LogQueue.LogQueue.Instance().queue) > 0:
                self.process_data()
                sys.stdout.write("SQL - BEFORE getLog, queue len: " + str(len(LogQueue.LogQueue.Instance().queue)) + '\n')
                sys.stdout.flush()
                LogQueue.LogQueue.Instance().getLog()
                sys.stdout.write("SQL - AFTER getLog, queue len: " + str(len(LogQueue.LogQueue.Instance().queue)) + '\n')
                sys.stdout.flush()

    def initSql(self):
        mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = configData["mysql"]["user"]
        app.config['MYSQL_DATABASE_PASSWORD'] = configData["mysql"]["password"]
        app.config['MYSQL_DATABASE_HOST'] = configData["mysql"]["url"]
        app.config['MYSQL_DATABASE_DB'] = configData["mysql"]["database"]
        mysql.init_app(app)
        self.cursor = mysql.connect().cursor()

    def process_data(self):
        sql = "SELECT * from WEBSITE;"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for website in data:
            sys.stdout.write("website: " + str(website) + '\n')
            sys.stdout.flush()
