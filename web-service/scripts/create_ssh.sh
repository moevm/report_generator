#!/usr/bin/env bash

mkdir "$HOME/www-data.ssh"
ssh-keygen -q -t rsa -f "$HOME/www-data.ssh/id_rsa" -N ""
chown -R www-data:www-data "$HOME/www-data.ssh"
mkdir /var/www/.ssh
touch /var/www/.ssh/config
chmod 666 /var/www/.ssh/config
{
  echo 'Host *'
  echo '     IdentityFile $HOME/www-data.ssh/id_rsa'
} > /var/www/.ssh/config
chown -R www-data:www-data /var/www/.ssh