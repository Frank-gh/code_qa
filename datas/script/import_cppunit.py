#!/usr/bin/python
#coding=utf8
"""
# Author: Frank
# Created Time : 2017-08-24 18:21:09

# File Name: import_cppunit.py
# Description:

"""

from xml.dom.minidom import parse
import sqlite3
import os
import sys, getopt


def help():
    print '''usage:
    -h help
    -f cppunit result file *.xml_file
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

c.execute('''CREATE TABLE CPPUNIT_FAILED 
        (ID INT PRIMARY KEY     NOT NULL,
        Name           TEXT,     
        Line           INT,
        FailureType    TEXT, 
        File           TEXT,
        Message            TEXT);
        ''')

c.execute('''CREATE TABLE CPPUNIT_SUCCESS 
        (ID INT PRIMARY KEY     NOT NULL,
        Name           TEXT);
        ''')

c.execute('''CREATE TABLE CPPUNIT_STATISTICS
        (Tests                INT,
        FailuresTotal         INT,
        Errors                INT,
        Failures              INT);
        ''')


dom = parse(xml_file)
TestRun = dom.documentElement

FailedTests = TestRun.getElementsByTagName("FailedTests")

for FailedTest in FailedTests:
    # id = FailedTest.getAttribute("id")
    a = FailedTest.getElementsByTagName("FailedTest")
    for f in a:
        id = f.getAttribute("id")
        Name = f .getElementsByTagName("Name")[0].childNodes[0].nodeValue
        FailureType = f .getElementsByTagName("FailureType")[0].childNodes[0].nodeValue
        Message = f .getElementsByTagName("Message")[0].childNodes[0].nodeValue
        Location = f .getElementsByTagName("Location")
        for l in Location:
            File = l.getElementsByTagName("File")[0].childNodes[0].nodeValue
            Line = l.getElementsByTagName("Line")[0].childNodes[0].nodeValue
    
        c.execute('''INSERT INTO CPPUNIT_FAILED (ID,Name,FailureType,File,'Line',Message)  VALUES ("''' 
        + id + '''","''' + Name + '''","''' + FailureType + '''","''' + File + '''","''' 
        + str(Line) + '''",''' + """'""" + Message  + """');""")

SuccessfulTests = TestRun.getElementsByTagName("SuccessfulTests")

for fulTests in SuccessfulTests:
    tests = fulTests.getElementsByTagName("Test")
    for t in tests:
        id = t.getAttribute("id")
        Name = t.getElementsByTagName("Name")[0].childNodes[0].nodeValue
        c.execute('''INSERT INTO CPPUNIT_SUCCESS (ID, NAME) VALUES ("''' 
        + id + '''","''' + Name +'''");''')

Statistics = TestRun.getElementsByTagName("Statistics")

for Statistic in Statistics:
    Tests = Statistic.getElementsByTagName("Tests")[0].childNodes[0].nodeValue
    FailuresTotal = Statistic.getElementsByTagName("FailuresTotal")[0].childNodes[0].nodeValue
    Errors = Statistic.getElementsByTagName("Errors")[0].childNodes[0].nodeValue
    Failures = Statistic.getElementsByTagName("Failures")[0].childNodes[0].nodeValue

    c.execute('''INSERT INTO CPPUNIT_STATISTICS (Tests,FailuresTotal,Errors,Failures) VALUES( '''
    + Tests + ',' + FailuresTotal + ',' + Errors + ',' + Failures + ');')

conn.commit()
conn.close()
