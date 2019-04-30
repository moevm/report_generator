FROM tknerr/baseimage-ubuntu:16.04
RUN apt-get update
RUN apt-get -y install nano
RUN apt-get -y install git


RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip


RUN apt-get -y install apache2 libapache2-mod-wsgi-py3
RUN apt-get clean

ADD ./ /report_generator
WORKDIR /report_generator
CMD /scripts/local_deploy.sh

CMD /etc/init.d/apache2 restart && /usr/sbin/sshd -D \
    -o UseDNS=no\
    -o UsePAM=no\
    -o PasswordAuthentication=yes\
    -o UsePrivilegeSeparation=no\
    -o PidFile=/tmp/sshd.pid

