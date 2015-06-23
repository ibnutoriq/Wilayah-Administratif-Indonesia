#!/bin/sh

DB_NAME=indonesia
DB_USER=root
DB_PASS='123456'

curl http://mfdonline.bps.go.id/index.php?link=hasil_pencarian --data "pilihcari=desa&kata_kunci=%25" > $DB_NAME.html
./parse.py $DB_NAME.html
rm $DB_NAME.html

mysql -u $DB_USER --password=$DB_PASS $DB_NAME < base_db.sql
mysqlimport --fields-terminated-by=, --local --verbose -u $DB_USER --password=$DB_PASS $DB_NAME ../csv/provinces.csv
mysqlimport --fields-terminated-by=, --local --verbose -u $DB_USER --password=$DB_PASS $DB_NAME ../csv/regencies.csv
mysqlimport --fields-terminated-by=, --local --verbose -u $DB_USER --password=$DB_PASS $DB_NAME ../csv/districts.csv
mysqlimport --fields-terminated-by=, --local --verbose -u $DB_USER --password=$DB_PASS $DB_NAME ../csv/villages.csv
mysqldump -u $DB_USER --password=$DB_PASS $DB_NAME > ../mysql/$DB_NAME.sql
