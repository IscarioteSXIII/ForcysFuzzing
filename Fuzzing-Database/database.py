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
        description='Fuzzer utilisant libinjection pour tester les injections SQL sur MariaDB & MySQL')
    parser.add_argument(
        '-t',
        '--type',
        dest='type',
        default='mysql',
        help=('Database type: mysql'),
        choices=["mysql","mariadb"])

#Options et arguments utilisés
    
    parser.add_argument('-q', '--query',dest='query',help='Query to fuzz',required=True)
    
    parser.add_argument('-p', '--payload',dest='payload',help='Payload to use',required=True)
    
    parser.add_argument('-c', '--chars',dest='chars',help='Characters to fuzz',required=True)
    
    parser.add_argument('--host',dest='host',help='Host to connect',required=True)
    
    parser.add_argument('-u', '--user',dest='user',help='Database user')
    
    parser.add_argument('--password',dest='password',help='Database user',default='')
    
    parser.add_argument('-d', '--db',dest='db',help='Database name',required=True)
    
    parser.add_argument('-o', '--out',dest='out',help='Filename pattern (default: log)',default="log")
    
    parser.add_argument('--log-all',dest='log_all',action='store_true')
    
    parser.add_argument('--check',dest='check',help='Check value',default=False)
    
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
            print(colorize("red", "[ERREUR] {}".format(err)))
            return None
        
    return connection

def get_next(string, args):
    if len(string) <= 0:
        string.append(args.chars[0])
    else:
        string[0] = args.chars[
            (args.chars.index(string[0]) + 1) % len(args.chars)]
        if args.chars.index(string[0]) == 0:
            return list(string[0]) + get_next(string[1:], args)
    return string

#Sauvegarde des informations dans un fichier log

def log_msg(filename, msg):
    lock.acquire()
    with open(filename, "a") as f:
        f.write("{}\n".format(msg))
    lock.release()

    
    
def process_one(opts):
    cursor = opts[0]
    payload = opts[1]
    args = opts[2]
    if os.path.isfile("{}_fp.txt".format(args.type)):
        fingerprints = open("{}_fp.txt".format(args.type), "r").read()
    else:
        fingerprints = list()

    if args.type in ["mysql", "mariadb"]:
        for item in cursor.execute(args.query.format(payload), multi=True):
            rows = item.fetchall()
    else:
        cursor.execute(args.query.format(payload))
        rows = cursor.fetchall()
    sqli = pylibinjection.detect_sqli(payload)
    msg = "Fingerprint: {} Query: {} Result: {}".format(
        sqli["fingerprint"], args.query.format(payload), rows)
    if len(rows) > 0:
        if sqli["sqli"]:
            print (colorize("red", "[BLOQUE] {}".format(msg)))
            if args.log_all:
                log_msg(
                    "{}_bad.txt".format(
                        args.type), "[{}] {}".format(
                        args.type.upper(), msg))
        else:
            if sqli["fingerprint"] in fingerprints:
                print (colorize("blue", "[OK][NON] {}".format(msg)))
                log_msg(
                    "{}_bad.txt".format(
                        args.type), "[NON][{}] {}".format(
                        args.type.upper(), msg))
            else:
                print (colorize("green", "[OK][Nouveau] {}".format(msg)))
                log_msg(
                    "{}_good.txt".format(
                        args.type), "[{}] {}".format(
                        args.type.upper(), msg))
                log_msg("{}_fp.txt".format(args.type), sqli["fingerprint"])
                fingerprints.append(sqli["fingerprint"])

#Connexion à la DB et cursor permettant l'injection des payloads
                
def main(args):
    cnx = db_connect(args)
    if not cnx:
        sys.exit()
    cursor = cnx.cursor()
    sequence = list()
    
#Tout logger (verbose)    
    
    if args.log_all:
        file_log = open("{}_all.txt".format(args.type), "w")
    if args.check:
        payload = args.payload.format(args.check)
        process_one([cursor, payload, args])
        sys.exit()
    else:
        while True:
            sequence = get_next(sequence, args)
            item = ''.join(reversed(sequence))
            if len(item) == 5:
                cnx.close()
                sys.exit()
            payload = args.payload.format(item)
            try:
                process_one([cursor, payload, args])
                
# Si erreur, rollback                
                
            except BaseException as err:
                if args.type == "pgsql":
                    cnx.rollback()
                if args.log_all:
                    log_msg(
                        "{}_all.txt".format(
                            args.type), "[{}] Query: {}".format(
                            args.type.upper(), args.query.format(payload)))
                continue


if __name__ == "__main__":
    args = parse_cli_args()
    main(args)



