#!/usr/bin/env python3.5

import sys
import json
from Singleton import Singleton

from  collections import deque
from threading import Thread

with open('./conf/config.json', 'r') as f:
	configData = json.load(f)

@Singleton
class LogQueue:
    def __init__(self):
        self.size = configData['queueSize']
        self.queue = deque(maxlen=self.size);

    def addLog(self, log):
        if (len(self.queue) >= self.size):
            sys.stdout.write("queue is full wait...\n")
            sys.stdout.flush()
            return False
        else:
            self.queue.append(log)
            sys.stdout.write("added item to queue\n")
            sys.stdout.flush()
            return True

    def getLog(self):
        return self.queue.popleft()
