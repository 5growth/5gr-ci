#!/bin/bash

GIT_MON="master"
GIT_SO="master"
GIT_VS="master"
GIT_RL="work_version"
GIT_CI="CDN_SSSA"

echo "Creating debugging user with password Username: user, Password: passw0rd"
adduser --quiet --disabled-password --shell /bin/bash --home /home/user --gecos "User with password ssh auth" user
echo "user:passw0rd" | chpasswd
echo "user ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/user

#exec 1 |tee log.log 2>&1
cd ~/

git clone https://github.com/denjuve/scripts > /dev/null 2>&1
echo "Installing docker..."
cd scripts && ./docker_install.sh  > /dev/null 2>&1 && echo "Docker installed"

echo '{  "insecure-registries" : ["img:5000"]}' > /etc/docker/daemon.json  #to mkb
systemctl restart docker && sleep 5

echo "Installing docker-compose"
sudo curl -s -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

mkdir -p -m 0777 /mnt/registry

echo "Cloning artifacts repo"
cd ~/ && git clone -b $GIT_CI https://5gr-ci:foirr%3B6Gri@5growth.eu/git/5growth.5gr-ci > /dev/null 2>&1 && echo "Artifact repo cloned (branch: $GIT_CI)"

echo "Starting private regestry"
sudo docker run -d -p 5000:5000   --restart=always   --name registry -v /mnt/registry:/var/lib/registry  registry:2

function script_mod {
sed -i 's/5growth.eu/5gr-ci:foirr%3B6Gri@5growth.eu/g' $1_build_docker.sh
sed -i 's/sudo docker-compose.*/sudo docker-compose build/g' $1_build_docker.sh
sed -i 's/${TAG}/local/g' docker-compose.y*ml
sed -i "s/GIT_BRANCH=.*/GIT_BRANCH=$2/" $1_build_docker.sh
}

cd ~/5growth.5gr-ci/containerization/monitoring_platform/		&& script_mod mon $GIT_MON && bash mon_build_docker.sh
cd ~/5growth.5gr-ci/containerization/rl			            		&& script_mod rl $GIT_RL && ./rl_build_docker.sh
cd ~/5growth.5gr-ci/containerization/so					            && script_mod so $GIT_SO && ./so_build_docker.sh
cd ~/5growth.5gr-ci/containerization/vertical_slicer/			  && script_mod vs $GIT_VS && ./vs_build_docker.sh

sudo docker images | grep local | awk '{print $1":"$2}' | xargs -I % sudo docker tag  %  "img:5000/"%
sudo docker images | grep 5000 | awk '{print $1":"$2}' | xargs -I % sudo docker push %

cd ~/5growth.5gr-ci/containerization/cfy/

cp docker-compose.yaml docker-compose.yaml.bkp
cat << EOF > docker-compose.yaml
version: "3"
services:
  cfy_mano_local:
    container_name: cfy_mano_local
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
      - ../rl/rl_git/rl/plugins/Cloudify/MTP_plugin/:/home/centos
    tmpfs:
      - /run
      - /run/lock
    restart: unless-stopped
    security_opt:
      - seccomp:unconfined
    network_mode: "host"
    cap_add:
      - SYS_ADMIN
    image: cloudifyplatform/community:latest
EOF

cat << EOF > cfy.sh
#!/bin/bash
sudo docker-compose up -d
sleep 3
sudo docker exec cfy_mano_local bash -c "until cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-openstack-plugin/2.14.7/cloudify_openstack_plugin-2.14.7-py27-none-linux_x86_64-centos-Core.wgn -y http://www.getcloudify.org/spec/openstack-plugin/2.14.7/plugin.yaml; do echo nicht; done"
sudo docker exec cfy_mano_local bash -c "until cfy plugins upload /home/centos/cloudify_mtp_plugin-0.0.1-centos-Core-py27.py36-none-linux_x86_64.wgn -y /home/centos/plugin.yaml; do echo nicht; done"
EOF

bash cfy.sh
