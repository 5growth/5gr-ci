FROM maven:3.6-jdk-11
#MAINTAINER

# Installing packages
RUN apt-get -y update

EXPOSE 8989

RUN mkdir -p /mon
ADD mon_git/config-manager-nxw /mon/config-manager-nxw
ADD mon_git/dep-kibana-dashboards-telca /mon/dep-kibana-dashboards-telca
WORKDIR /mon/dep-kibana-dashboards-telca
RUN mvn clean install -Dmaven.test.skip=true -Dmaven.javadoc.skip=true
WORKDIR /mon/config-manager-nxw
RUN mvn clean package -Dmaven.test.skip=true -Dmaven.javadoc.skip=true
RUN rm -rf ~/.m2/repository
# COPY mon_app/config.properties /mon/config-manager-nxw
COPY mon_app/configure_grafana.sh /mon/config-manager-nxw/configure_grafana.sh
RUN chmod o+x /mon/config-manager-nxw/configure_grafana.sh
CMD ./configure_grafana.sh mon_grafana

