#!/usr/bin/env bash

sudo -u www-data ssh -T git@github.com
service mongodb start
service apache2 restart
