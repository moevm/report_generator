FROM tknerr/baseimage-ubuntu:18.04

RUN apt-get -y install locales
RUN apt-get install -y language-pack-ru
ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales


RUN apt-get update
RUN apt-get -y install git

RUN apt-get -y install apache2=2.4.29-1ubuntu4.8  apache2-dev=2.4.29-1ubuntu4.8  mongodb
RUN apt-get -y install python3.6  python3-dev  python3-pip  python3-flask  vim  nano curl

#RUN apt-get -y install unoconv
RUN apt-get -y install libreoffice

RUN pip3 install --upgrade pip
RUN pip3 install mod_wsgi
RUN mod_wsgi-express module-config > /etc/apache2/mods-available/wsgi.load
RUN a2enmod wsgi


ADD ./ /report_generator
WORKDIR /report_generator
RUN ./scripts/local_deploy.sh
RUN ./scripts/create_ssh.sh

CMD service mongodb start && /etc/init.d/apache2 restart && /usr/sbin/sshd -D \
    -o UseDNS=no\
    -o UsePAM=no\
    -o PasswordAuthentication=yes\
    -o UsePrivilegeSeparation=no\
    -o PidFile=/tmp/sshd.pid
