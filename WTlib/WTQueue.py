#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import threading


class Queue(object):

    def __init__(self):
        self.sema = threading.BoundedSemaphore(value=1)
        self.queue = []

    def put(self, item, priority):
        with self.sema:
            self.queue.append((priority, item))
            self.queue.sort(key=lambda job: job[0])

    def get(self):
        with self.sema:
            if not self.isEmpty():
                return self.queue.pop()[1]
            return None

    def remove(self, item):
        with self.sema:
            self.queue = []
            for element in filter(lambda job: job[1] != item, self.queue):
                self.queue.append(element)

    def isEmpty(self):
        return len(self.queue) <= 0
