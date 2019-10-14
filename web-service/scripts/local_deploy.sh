#!/usr/bin/env bash

python3.6 -m pip install -r ./scripts/requirements.txt
pip3.6 install mod_wsgi
mod_wsgi-express module-config > /etc/apache2/mods-available/wsgi.load
a2enmod wsgi

CATALOG='report_generator'
HOSTS_STRING="127.0.0.1       report_generator"
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
cp ./src/*.sh /var/www/"$CATALOG"
cp ./src/*.txt /var/www/"$CATALOG"
cp -r ./src/google /var/www/"$CATALOG"
cp -r ./src/static /var/www/"$CATALOG"/static/
cp -r ./src/templates /var/www/"$CATALOG"/templates/
cp -r ./src/word_templates /var/www/"$CATALOG"/word_templates
cp ./src/config/"${CONFIG}" /etc/apache2/sites-available/
cp -r ./src/services /var/www/"$CATALOG"/services/

chown -R www-data:www-data /var/www/"$CATALOG"
a2ensite "${CONFIG}"
a2dissite 000-default.conf
service apache2 restart