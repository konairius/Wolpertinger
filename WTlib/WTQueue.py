#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'


class Queue(object):

    def __init__(self):
        self.queue = []

    def put(self, item, priority):
        self.queue.append((priority, item))
        self.queue.sort(key=lambda job: job[0])

    def get(self):
        return self.queue.pop()

    def remove(self, item):
        self.queue = []
        for element in filter(lambda job: job[1] != item, self.queue):
            self.queue.append(element)
