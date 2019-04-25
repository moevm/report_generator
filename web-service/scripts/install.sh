#!/usr/bin/env bash
./scripts/local_deploy.sh
a2dissite 000-default.conf
service apache2 reload