#!/usr/bin/env python
# -*- coding: ascii -*-

"""
Wolpertinger Filehashing lib

"""

__author__ = 'Konstantin Renner (rennerkonsti@gmail.com)'
__copyright__ = 'Copyright (c) 2012 Konstantin Renner'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import sqlite3
import logging

logger = logging.getLogger(__name__)

database = sqlite3.connect('cache.sqlite')


class CacheMissError(Exception):
    pass


class Cache(object):

    def __init__(self, cacheType):
        self.cacheType = cacheType
        # the Cached object must implement this static Method
        self.fields = cacheType.serializable()
        createStatement = 'CREATE TABLE IF NOT EXISTS '
        createStatement += str(cacheType)[8:-2].replace('.', '_') + '('
        for field, dataType in self.fields:
            createStatement += str(field) + ' '
            createStatement += str(dataType) + ', '
        createStatement = createStatement[:-2]
        createStatement += ')'
        logger.debug(createStatement)
        cursor = database.cursor()
        cursor.execute(createStatement)
        database.commit()
        cursor.close()

    def add(self, newObject):
        if not type(newObject) == self.cacheType:
            raise TypeError('This cache is of type ' + str(self.cacheType))
        serialized = newObject.serialize()
        insertStatement = 'INSERT INTO '
        insertStatement += str(type(newObject))[8:-2].replace('.', '_')
        insertStatement += ' VALUES ( '
        for value in serialized:
            insertStatement += '"' + str(value) + '"' + ', '
        insertStatement = insertStatement[:-2]
        insertStatement += ')'
        logger.debug(insertStatement)
        cursor = database.cursor()
        cursor.execute(insertStatement)
        database.commit()
        cursor.close()

    def get(self, getDict):
        getStatement = 'SELECT * FROM '
        getStatement += str(self.cacheType)[8:-2].replace('.', '_')
        getStatement += ' WHERE '
        for key in list(getDict):
            getStatement += '"' + key + '"'
            getStatement += ' = '
            getStatement += '"' + getDict[key] + '"'
            getStatement += ' AND '
        getStatement = getStatement[:-5]
        logger.debug(getStatement)
        cursor = database.cursor()
        cursor.execute(getStatement)
        buildDict = dict()
        
        result = cursor.fetchall()
        if len(result) < 1:
            raise CacheMissError()
        i = 0
        for value in result[0]:
            buildDict[self.fields[i][0]] = value
            i += 1
        return self.cacheType.deserialize(buildDict)

    def remove(self, delObject):
        pass
