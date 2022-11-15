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


#Arguments et options permettant de choisir la BDD à fuzzer, qu'elle soit locale ou distante

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
    
