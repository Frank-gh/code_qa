#########################################################################
# File Name: import.sh
# Author: Frank
# mail: frank.x@aliyun.com
# Created Time: 2017-08-24 21:51:15
#########################################################################
#!/bin/bash

set -e

function help()
{
    echo "usage:
    -h help
    -c cppcheck result file *.xml
    -u cppunit result file *.xml
    -v valgrind result file *.xml
    -d import sqlite3 db file *.db"
}

while getopts "c:u:v:d:h" arg
do
    case $arg in
        c)
        check_file=$OPTARG
        ;;
        u)
        unit_file=$OPTARG
        ;;
        v)
        valgrind_file=$OPTARG
        ;;
        d)
        db_file=$OPTARG
        ;;
        h)
        help
        exit 1
        ;;
        ?)
        help
        exit 1
        ;;
    esac
done


if  [ ! -n "$check_file" -o ! -n "$unit_file" -o ! -n "$valgrind_file" -o ! -n "$db_file" ] ;then
    help
    exit 1
fi

rm -rf $db_file


python import_cppcheck.py -f $check_file -d $db_file
python import_cppunit.py -f $unit_file -d $db_file
python import_valgrind.py -f $valgrind_file -d $db_file

