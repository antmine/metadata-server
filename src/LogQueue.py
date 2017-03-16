#!/usr/bin/env python3.5

import sys
import json

from  collections import deque
from threading import Thread

class LogQueue:

    size = 0;

    def __init__(self, size):
        self.size = size

    queue = deque(maxlen=size);

    def addLog(self, log):
        print ("adding item to queue of size:" + str(self.size))
        if (len(self.queue) >= self.size):
            print ("queue is full wait...")
            return False
        else:
            self.queue.append(log)
            print ("added item to queue")
            return True

    def getLog(self):
        return self.queue.popleft()
