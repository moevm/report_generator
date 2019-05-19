FROM tknerr/baseimage-ubuntu:18.04
RUN apt-get update
RUN apt-get -y install nano
RUN apt-get -y install git

RUN apt-get -y install apache2=2.4.29-1ubuntu4.6  apache2-dev=2.4.29-1ubuntu4.6  mongodb  python3.6  python3-dev  python3-pip  python3-flask  vim  nano curl unoconv
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade Flask

RUN pip3 install --upgrade pip
RUN pip3 install mod_wsgi
RUN mod_wsgi-express module-config > /etc/apache2/mods-available/wsgi.load
RUN a2enmod wsgi


ADD ./ /report_generator
WORKDIR /report_generator
RUN ./scripts/local_deploy.sh
RUN ./scripts/create_ssh.sh
WORKDIR /var/www/report_generator

CMD /etc/init.d/apache2 restart && /usr/sbin/sshd -D \
    -o UseDNS=no\
    -o UsePAM=no\
    -o PasswordAuthentication=yes\
    -o UsePrivilegeSeparation=no\
    -o PidFile=/tmp/sshd.pid