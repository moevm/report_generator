FROM tknerr/baseimage-ubuntu:18.04

RUN apt-get -y install locales
RUN apt-get install -y language-pack-ru
ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales

RUN apt-get update
RUN apt-get -y install git

RUN apt-get -y install apache2  apache2-dev  mongodb
RUN apt-get -y install python3.6  python3-dev  python3-pip  python3-flask  vim  nano curl
RUN pip3 install --upgrade pip


ADD ./ /report_generator
WORKDIR /report_generator
RUN ./scripts/install_libreoffice.sh
RUN ./scripts/local_deploy.sh
RUN ./scripts/create_ssh.sh

CMD service mongodb start && /etc/init.d/apache2 restart && /usr/sbin/sshd -D \
    -o UseDNS=no\
    -o UsePAM=no\
    -o PasswordAuthentication=yes\
    -o UsePrivilegeSeparation=no\
    -o PidFile=/tmp/sshd.pid
