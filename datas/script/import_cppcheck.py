#!/usr/bin/python
#coding=utf8
"""
# Author: frank
# Created Time : 2017-08-20 14:46:49

# File Name: import_cppcheck.py
# Description:

"""

from xml.dom.minidom import parse
import sqlite3
import os
import sys, getopt

def help():
    print '''usage:
    -h help
    -f cppcheck result file *.xml_file
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

# if os.path.exists(db_file):
#     os.remove(db_file)

conn = sqlite3.connect(db_file)
c = conn.cursor()

c.execute('''CREATE TABLE CPPCHECK_RESULT 
        (ID INT PRIMARY KEY     NOT NULL,
        FILE           TEXT,     
        LINE           INT, 
        TYPE           TEXT     NOT NULL,
        SEVERITY       TEXT     NOT NULL,
        MSG            TEXT     NOT NULL);
        ''')

id = 0
#打开xml文件
dom = parse(xml_file)

results = dom.documentElement
errors = results.getElementsByTagName("error") 
for error in errors:
    id = id + 1
    if error.getAttribute("file"):
        f_file = error.getAttribute("file")
    else:
        f_file = ''

    if error.getAttribute("line"):
        f_line = error.getAttribute("line")
    else:
        f_line = 0
    c.execute ('''INSERT INTO CPPCHECK_RESULT (ID,FILE,LINE,TYPE,SEVERITY,MSG)  
VALUES (''' + str(id) + ''',"''' + f_file + '''",''' +  str(f_line) + ''',"''' + error.getAttribute("id") + '''","''' +  error.getAttribute("severity") + '''","''' +  error.getAttribute("msg") + '''");''')


conn.commit()
conn.close()


