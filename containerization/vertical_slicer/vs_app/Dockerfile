FROM maven:3-jdk-8
#MAINTAINER
#ENV POSTGRES_VERSION 9.4
# Installing packages


#RUN apt-get update && rm -rf /var/lib/apt/lists/* && apt-get install --no-install-recommends -y netcat software-properties-common supervisor apache2 php7.0
RUN apt-get update 
RUN apt-get install -y netcat software-properties-common supervisor apache2 php7.0

ADD vs_app/apache2.conf /etc/apache2/apache2.conf
ADD vs_app/ssi.conf /etc/apache2/conf-available/ssi.conf
ADD vs_app/000-default.conf /etc/apache2/sites-available/000-default.conf

RUN a2enconf ssi
RUN a2enmod include
#
ADD vs_app/supervisord-apache2.conf /etc/supervisor/conf.d/supervisord-apache2.conf
ADD vs_app/supervisord-apache2.sh /supervisord-apache2.sh
ADD vs_app/start.sh /start.sh
RUN chmod 755 /*.sh

RUN mkdir -p /www && rm -fr /var/www && ln -s /www /var/www

EXPOSE 80 8082 5005


RUN mkdir -p /vs
ADD vs_git /vs
RUN mkdir -p /vs/lib

#RUN git clone -b feat-librefactor https://github.com/nextworks-it/nfv-ifa-libs/
#WORKDIR nfv-ifa-libs
#RUN mvn clean install
WORKDIR /vs/lib
#Changed according to VS R1 README
#RUN git clone -b feat-librefactor https://github.com/nextworks-it/nfv-ifa-libs
#WORKDIR /vs/lib/nfv-ifa-libs
#RUN mvn clean install -Dmaven.test.skip=true
RUN git clone -b dev_5growth https://github.com/nextworks-it/nfv-ifa-libs/
WORKDIR /vs/lib/nfv-ifa-libs
RUN git checkout b34fcb3
RUN mvn clean install -Dmaven.test.skip=true
WORKDIR /vs/lib



# nfv-sol-libs sections removed see VS R1 README
#RUN git clone https://github.com/nextworks-it/nfv-sol-libs
##WORKDIR nfv-sol-libs
##RUN /bin/bash install_nfv_sol_libs.sh
######################################################
##RUN git clone https://github.com/nextworks-it/nfvo-drivers
##WORKDIR nfvo-drivers
##RUN mvn clean install
#WORKDIR /vs/lib/nfv-sol-libs
#RUN mkdir -p /vs/lib/nfv-sol-libs/lib
#RUN /bin/bash install_nfv_sol_libs.sh lib
#WORKDIR /vs/lib
##############################################################
RUN git clone https://github.com/nextworks-it/slicer-identity-mgmt
#WORKDIR slicer-identity-mgmt/
#RUN mvn clean install
WORKDIR /vs/lib/slicer-identity-mgmt
RUN git checkout 32b04e3
RUN mvn clean install -Dmaven.test.skip=true

##Accordin to readme nfvo-drivers is in 5Growth-VS repo/NFVO_DRIVERS
WORKDIR /vs/NFVO_DRIVERS
RUN git checkout ee006a4
RUN mvn clean install
WORKDIR /vs/lib


RUN git clone -b 5growth-release https://github.com/nextworks-it/slicer-catalogue
#WORKDIR slicer-catalogue
#RUN mvn clean install
WORKDIR /vs/lib/slicer-catalogue
RUN git checkout e0784bb
RUN mvn clean install -Dmaven.test.skip=true
WORKDIR /vs
# RUN rm -r /vs/lib

WORKDIR /vs/FIVEGEVE_REST_CLIENTS
RUN mvn clean install -Dmaven.test.skip=true

WORKDIR /vs/SEBASTIAN
RUN mvn package -Dmaven.test.skip=true
#WORKDIR /vs/SEBASTIAN/target
WORKDIR /vs/SEBASTIAN/SEBASTIAN_CORE/target
# RUN rm -rf ~/.m2/repository
CMD ["/start.sh"]
