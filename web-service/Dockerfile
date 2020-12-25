FROM tknerr/baseimage-ubuntu:18.04

HEALTHCHECK --interval=60s --timeout=5s CMD curl --fail http://localhost:80/ || exit 1

RUN apt-get -y install locales
RUN apt-get install -y language-pack-ru
ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN locale-gen ru_RU.UTF-8 && dpkg-reconfigure locales

RUN apt-get update && apt-get install -y \
	git \
	apache2 \
	apache2-dev \
	python3.6 \
	python3-dev \
	python3-pip \
	python3-flask \
	vim  \
	nano \
	curl \
	libreoffice \
	&& rm -rf /var/lib/apr/lists/*
RUN pip3 install --upgrade pip

ADD ./ /report_generator
WORKDIR /report_generator
RUN ./scripts/local_deploy.sh
RUN ./scripts/create_ssh.sh
RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
RUN ./scripts/init.sh

CMD apachectl -D FOREGROUND
