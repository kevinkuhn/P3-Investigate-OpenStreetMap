#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_db():
    # start MongoClient
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    # 'maps' here is the database name. It will be created if it does not exist.
    db = client.citties
    return db