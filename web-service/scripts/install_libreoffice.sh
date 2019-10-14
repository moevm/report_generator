#!/usr/bin/env bash

wget http://downloadarchive.documentfoundation.org/libreoffice/old/5.1.6.2/deb/x86_64/LibreOffice_5.1.6.2_Linux_x86-64_deb.tar.gz
tar -xzvf LibreOffice_5.1.6.2_Linux_x86-64_deb.tar.gz
dpkg -i LibreOffice_5.1.6.2_Linux_x86-64_deb/DEBS/*.deb
apt-get -y install libxinerama1
apt-get -y install libcairo2
apt-get -y install libcups2
apt-get -y install libdbus-glib-1.2
apt-get -y install libGL.1

