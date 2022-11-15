#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import pylibinjection
import threading
from multiprocessing.pool import ThreadPool as Pool
lock = threading.Lock()


#Colorisation du texte permettant une meilleure compréhension des résultats affichés

def colorize(color, text):
    if color == 'red':
        return ''.join(['\033[1;31m', text, '\033[1;m'])
    elif color == 'green':
        return ''.join(['\033[1;32m', text, '\033[1;m'])
    elif color == 'blue':
        return ''.join(['\033[1;34m', text, '\033[1;m'])
    else:
        return text


#

def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Fuzzer libinjection pour MariaDB, MSSQL, \
            MySQL, PostgreSQL and Oracle DB')
    parser.add_argument(
        '-t',
        '--type',
        dest='type',
        default='mysql',
        help=('Database type: mysql'),
        choices=[
            "mysql",
            "mariadb"])
    
    #
    
    parser.add_argument('-q', '--query',
                        dest='query',
                        help='Query to fuzz',
                        required=True)
    parser.add_argument('-p', '--payload',
                        dest='payload',
                        help='Payload to use',
                        required=True)
    parser.add_argument('-c', '--chars',
                        dest='chars',
                        help='Characters to fuzz',
                        required=True)
    parser.add_argument('--host',
                        dest='host',
                        help='Host to connect',
                        required=True)
    parser.add_argument('-u', '--user',
                        dest='user',
                        help='Database user')
    parser.add_argument('--password',
                        dest='password',
                        help='Database user',
                        default='')
    parser.add_argument('-d', '--db',
                        dest='db',
                        help='Database name',
                        required=True)
    parser.add_argument('-o', '--out',
                        dest='out',
                        help='Filename pattern (default: log)',
                        default="log")
    parser.add_argument('--log-all',
                        dest='log_all',
                        action='store_true')
    parser.add_argument('--check',
                        dest='check',
                        help='Check value',
                        default=False)
    return parser.parse_args()


#Connecteurs permettant de se connecter aux différentes BDD (MariaDB)

def db_connect(args):
    if args.type == "mysql" or args.type == "mariadb":
        import mysql.connector
        try:
            connection = mysql.connector.connect(
                user=args.user,
                password=args.password,
                database=args.db,
                host=args.host)
        except mysql.connector.Error as err:
            print(colorize("red", "[ERROR] {}".format(err)))
            return None


    return connection


