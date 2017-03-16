#!/usr/bin/env python3.5

import sys
import json
import logging
import LogQueue
import threading
import run as main
from collections import deque
from flask import Flask, jsonify, make_response, request, abort
from flask.ext.classy import FlaskView

configData = json.loads(json.dumps(main.configData))
#queue = LogQueue.LogQueue(configData["queueSize"])

class serverReception(threading.Thread, FlaskView):

	logger = logging.basicConfig(filename='logFile.log', level=logging.INFO)
	app = Flask(__name__)

	def __init__(self):
		threading.Thread.__init__(self)
		self.app.run(host= configData["host"], port= configData["port"])

	@app.after_request
	def after_request(data):
		response = make_response(data)
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
		response.headers['Access-Control-Allow-Methods'] = 'POST'
		return response

	@app.errorhandler(400)
	def bad_request(error):
		return make_response(jsonify( { 'error': 'Bad Request' } ), 400)

	@app.errorhandler(404)
	def not_found(error):
		return make_response(jsonify( { 'error': 'Not Found' } ), 404)

	@app.route('/log', methods = ['POST'])
	def create_log():
		print (request.json)
		if main.queue.addLog(request.json):
			print (main.queue.queue)
			return make_response(jsonify( { 'succes': 'Ok' } ), 200)
		else:
			return make_response(jsonify({'error': 'Service Unavailable - Queue is full'}), 503)
