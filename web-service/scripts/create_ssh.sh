#!/usr/bin/env bash

mkdir "$HOME/www-data.ssh"
ssh-keygen -q -t rsa -f "$HOME/www-data.ssh/id_rsa" -N ""
sudo chown -R www-data:www-data "$HOME/www-data.ssh"
sudo mkdir /var/www/.ssh
sudo touch /var/www/.ssh/config
sudo chmod 666 /var/www/.ssh/config
{
  sudo echo 'Host *'
  sudo echo '     IdentityFile $HOME/www-data.ssh/id_rsa'
} > /var/www/.ssh/config
sudo chown -R www-data:www-data /var/www/.ssh

