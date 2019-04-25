#!/usr/bin/env bash

pip3 install -r scripts/requirements.txt

CATALOG='report_generator'
HOSTS_STRING="127.0.1.1       report_generator"
CONFIG=$CATALOG.conf

if ! grep -Fxq "$HOSTS_STRING" /etc/hosts
then
    echo "$HOSTS_STRING" >> /etc/hosts
fi

rm -rf /var/www/"$CATALOG"
mkdir /var/www/"$CATALOG"

cp ./src/*.py  /var/www/"$CATALOG"
cp ./src/*.json  /var/www/"$CATALOG"
cp ./src/"$CATALOG".wsgi /var/www/"$CATALOG"
cp -r ./src/static /var/www/"$CATALOG"/static/
cp -r ./src/templates /var/www/"$CATALOG"/templates/
cp -r ./src/word_templates /var/www/"$CATALOG"/word_templates
cp ./src/config/"${CONFIG}" /etc/apache2/sites-available/

chown -R www-data:www-data /var/www/"$CATALOG"
a2ensite "${CONFIG}"
service apache2 restart