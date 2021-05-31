package com.libs

def instCfy_conf(cfyCtl_ip, depl_Id) {
string cfyCtl = cfyCtl_ip

sh '''
    rm -rf Dockerfile || true
    rm -rf *.yml || true
    sudo docker-compose down || true
    sudo docker system prune -a -f || true
'''

  sh """
cat > Dockerfile << EOF
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y wget
RUN wget http://repository.cloudifysource.org/cloudify/19.07.18/community-release/cloudify-cli-community-19.07.18.deb
RUN dpkg -i *.deb
RUN mkdir infraDev
COPY infra.yml infraDev

#RUN cfy profiles use $cfyCtl -u admin -p admin -t default_tenant
#RUN cfy profiles use ${cfyCtl_ip} -u admin -p admin -t default_tenant
#RUN cfy install infraDev/infra.yml -b ${depl_Id}
#RUN cfy deployments outputs ${depl_Id} | grep -i value | awk '{print \$2}' | tee ${depl_Id}.IP
EOF
  """
    sh """
cat > docker-compose.yml << EOF
version: '3'
services:
  cfydev:
    container_name: cfydev
    image: ubuntu:latest
    build:
      context: .
      dockerfile: ./Dockerfile
    command: cfy profiles use ${cfyCtl_ip} -u admin -p admin -t default_tenant; cfy install infraDev/infra.yml -b ${depl_Id}; cfy deployments outputs ${depl_Id} | grep -i value | awk '{print \$2}' | tee ${depl_Id}.IP
EOF
"""
}
return this