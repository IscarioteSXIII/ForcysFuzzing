English

This script has been created to test database and to find if they're vulnerable to SQL Injection.
Actually, only MariaDB and MySQL are supported implementatioon of other technologies will be possible with further work (OracleDB, MSSQL, PostgreSQL...)


## Help
```
# python3 database.py -h 
usage: database.py [-h] --host [hostame/IP] [-t {mysql,mariadb}] -q QUERY -p
                 PAYLOAD -c CHARS [-u USER] [--password PASSWORD] -d DB
                 [-o OUT] [--log-all] [--check CHECK] [--threads THREADS]

optional arguments:
  -h, --help            show help
  --host HOST           Hostname or IP to test
  -t {mysql,mariadb}, --type {mysql,mariadb}
                        Database type: mysql, mariadb
  -q QUERY, --query QUERY
                        Query to fuzz
  -p PAYLOAD, --payload PAYLOAD
                        Payload to use
  -c CHARS, --chars CHARS
                        Characters to fuzz
  -u USER, --user USER  Database user
  --password PASSWORD   Database password
  -d DB, --db DB        Database name
  -o OUT, --out OUT     Filename pattern (default: log)
  --log-all
  --check CHECK         Check value
```

## Usage example
```
python3 database.py --host 10. 10.10.1 -t mariadb -u admin -d test --log-all -q "select * from users where id='1{}'" -c " \"#\$%&()*+,-./1:;<=>?@[\]^_\`a{|}~!" -p "' + {} union select 'a',version() -- 1"
```
