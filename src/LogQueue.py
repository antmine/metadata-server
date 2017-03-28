#!/usr/bin/env python3.5

import sys
import json
from Singleton import Singleton

from  collections import deque
from threading import Thread

configFilePath =  None;

if (os.envrion['CONFIG_FILE'])
	configFilePath = os.envrion['CONFIG_FILE']
else
	configFilePath = './conf/config.json'

with open(configFilePath, 'r') as f:
	configData = json.load(f)

@Singleton
class LogQueue:
    def __init__(self):
        self.size = configData['queueSize']
        self.queue = deque(maxlen=self.size);

    def addLog(self, log):
        if (len(self.queue) >= self.size):
            return False
        else:
            self.queue.append(log)
            return True

    def getLog(self):
        return self.queue.popleft()
