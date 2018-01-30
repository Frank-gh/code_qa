#!/usr/bin/python
#coding=utf8
"""
# Author: frank
# Created Time : 2017-08-20 16:40:36

# File Name: import_valgrind.py
# Description:

"""

from xml.dom.minidom import parse
import sqlite3
import sys, getopt 


def help():
    print '''usage:
    -h help
    -f valgrind result file *.xml_file
    -d import sqlite3 db file *.db'''
    sys.exit(1)

opts, args = getopt.getopt(sys.argv[1:], "hf:d:")

xml_file = ''
db_file = ''

for op, value in opts:
    if op == "-f":
        xml_file = value
    elif op == "-d":
        db_file = value
    elif op == "-h":
        help()

if xml_file == '' or db_file == '':
    help()

conn = sqlite3.connect(db_file)
c = conn.cursor()

c.execute('''CREATE TABLE VALGRIND_RESULT 
        (ID INT PRIMARY KEY     NOT NULL,
        OBJ            TEXT,     
        DIR            TEXT,
        FILE           TEXT,
        FN             TEXT,
        LINE           INT ); 
        ''')

dom = parse('v.xml')

root = dom.documentElement

id = 0

errors = root.getElementsByTagName("error")
for error in errors:
    stacks = error.getElementsByTagName("stack")
    for stack in stacks:
        frames = stack.getElementsByTagName("frame")
        for frame in frames:
            id = id + 1
            line = 0
            obj = ''
            fn = ''
            dir = ''
            file = ''
            if frame.getElementsByTagName("line"):
                line = frame.getElementsByTagName("line")[0].childNodes[0].nodeValue
            else:
                continue

            if frame.getElementsByTagName("obj"):
                obj = frame.getElementsByTagName("obj")[0].childNodes[0].nodeValue

            if frame.getElementsByTagName("fn"):
                fn = frame.getElementsByTagName("fn")[0].childNodes[0].nodeValue

            if frame.getElementsByTagName("dir"):
                dir = frame.getElementsByTagName("dir")[0].childNodes[0].nodeValue
            
            if frame.getElementsByTagName("file"):
                file = frame.getElementsByTagName("file")[0].childNodes[0].nodeValue

            c.execute('''INSERT INTO VALGRIND_RESULT (ID,OBJ,DIR,FILE,FN,LINE) VALUES (''' + str(id) + ''',"''' 
                    + obj + '''","''' + dir + '''","''' + file + '''","''' + fn + '''",''' + str(line) + ''');''')


conn.commit()
conn.close()

