FROM tknerr/baseimage-ubuntu:16.04
RUN apt-get update
RUN apt-get -y install nano
RUN apt-get -y install git


RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip

RUN apt-get clean && apt-get update
RUN apt-get -y install apache2 apache2-dev
RUN python3.6 -m pip install -v mod_wsgi-httpd
RUN python3.6 -m pip install mod_wsgi
RUN apt-get clean

ADD ./ /report_generator
WORKDIR /report_generator
RUN  mod_wsgi-express module-config
#RUN a2enmod wsgi
RUN ./scripts/local_deploy.sh

CMD /etc/init.d/apache2 restart && /usr/sbin/sshd -D \
    -o UseDNS=no\
    -o UsePAM=no\
    -o PasswordAuthentication=yes\
    -o UsePrivilegeSeparation=no\
    -o PidFile=/tmp/sshd.pid