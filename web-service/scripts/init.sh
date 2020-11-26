#!/usr/bin/env bash

sudo -u www-data ssh -T git@github.com
service apache2 restart
