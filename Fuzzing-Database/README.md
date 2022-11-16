English

This script has been created to test database and to find if they're vulnerable to SQL Injection.
Actually, only MariaDB and MySQL are supported. Implementatioon of other technologies will be possible with further work (OracleDB, MSSQL, PostgreSQL...)


## Help
```
# python3 database.py -h 
usage: database.py [-h] --host [hostame/IP] [-t {mysql,mariadb}] -q QUERY -p
                 PAYLOAD -c CHARS [-u USER] [--password PASSWORD] -d DB
                 [-o OUT] [--log-all] [--check CHECK] [--threads THREADS]

optional arguments:
  -h, --help                   help
  --host HOST                  Hostname or IP to test
  -t TYPE, --type              Database type: mysql, mariadb
  -q QUERY, --query            Query to fuzz
  -p PAYLOAD, --payload        Payload to use
  -c CHARS, --chars            Characters to fuzz
  -u USER, --user              Database user
  --password                   Database password
  -d DB, --db                  Database name
  -o OUT, --out                Filename
  --log-all                    Log everything
  --check                      Check value
```

## Usage example
```
python3 database.py --host 10. 10.10.1 -t mariadb -u admin -d test --log-all -q "select * from users where id='1{}'" -c " \"#\$%&()*+,-./1:;<=>?@[\]^_\`a{|}~!" -p "' + {} union select 'a',version() -- 1"
```
