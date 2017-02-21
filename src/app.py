#!/usr/bin/env python3

import sys
import json

from collections import deque
from threading import Thread
from flask import Flask, jsonify, make_response, request, abort

with open('./conf/config.json', 'r') as f:
	configData = json.load(f)

queue = deque(maxlen=configData["queueSize"])

class serverReception():

	app = Flask(__name__)

	@app.after_request
	def after_request(data):
		response = make_response(data)
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
		response.headers['Access-Control-Allow-Methods'] = 'POST'
		return response

	tasks = []

	@app.errorhandler(400)
	def bad_request(error):
		return make_response(jsonify( { 'error': 'Bad Request' } ), 400)

	@app.errorhandler(404)
	def not_found(error):
		return make_response(jsonify( { 'error': 'Not Found' } ), 404)

	@app.route('/log', methods = ['POST'])
	def create_log():
		print (request.json)
		queue.appendleft(request.json)
		print (queue)
		return 'OK'

if __name__ == '__main__':
	server = serverReception()
	server.app.run(host= configData["host"], port= configData["port"])
	thread = Thread(target = server)
	thread.start()
	print ("thread serverReception finished")
