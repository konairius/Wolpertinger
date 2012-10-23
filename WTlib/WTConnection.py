#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Unittest

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.1.1'

import logging


logger = logging.getLogger(__name__)


class Connection(object):

    def __init__(self, localURI, remoteURI):
        self.localURI = localURI
        self.remoteURI = remoteURI
