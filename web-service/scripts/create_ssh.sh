#!/usr/bin/env bash

mkdir /var/www/.ssh
touch /var/www/.ssh/config
{
  echo 'Host github.com'
  echo '  Hostname ssh.github.com'
  echo '  Port 443'
} > /var/www/.ssh/config
chmod 600 /var/www/.ssh/config
chown -R www-data:www-data /var/www/.ssh
chown -R www-data:www-data /var/www

