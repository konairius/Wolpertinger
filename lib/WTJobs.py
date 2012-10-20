#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Paralell execution helper for Wolpertinger


Jobs have to implement the start(self) method:

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.2' #Versioning: http://www.python.org/dev/peps/pep-0386/

import Queue
import threading

queue = Queue.Queue()

def startWorkers(numberOfWorkers):
	for i in range(numberOfWorkers):
		t = threading.Thread(target=worker)
		t.daemon = True
		t.start()

def worker():
	global localCopyQueue
	while True:
		currentTask = queue.get()
		currentTask.start()
		queue.task_done()
