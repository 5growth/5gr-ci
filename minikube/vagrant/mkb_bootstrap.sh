#!/bin/bash
GIT_CI="master"
echo "Creating debugging user with password Username: user, Password: passw0rd"
adduser --quiet --disabled-password --shell /bin/bash --home /home/user --gecos "User with password ssh auth" user
echo "user:passw0rd" | chpasswd
echo "user ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/user

echo "Updating system..."
sudo apt update > /dev/null 2>&1
sudo apt upgrade -y > /dev/null 2>&1
echo "Installing prerequisites.."
sudo apt install -y apt-transport-https gnupg2 conntrack > /dev/null 2>&1
git clone https://github.com/denjuve/scripts > /dev/null 2>&1
echo "Installing docker..."
cd scripts && ./docker_install.sh > /dev/null 2>&1

echo '{  "insecure-registries" : ["img:5000"]}' > /etc/docker/daemon.json  #to mkb
systemctl restart docker

echo "Installing kubectl..."
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update > /dev/null 2>&1
sudo apt-get install -y kubectl > /dev/null 2>&1
#kubectl version --client

echo "Install minikube..."
curl -sLo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube

sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/

sudo -E minikube start --vm-driver=none

sudo -i -u vagrant bash << EOF
sudo cp -r /root/.kube $HOME && sudo cp -r /root/.minikube $HOME
sudo chown -R $USER:$USER $HOME/.kube $HOME/.minikube
EOF

#&v
git clone https://github.com/5growth/5gr-ci
for file in $(ls *.y*aml)
do
#&v
sed -i "s&https://github.com/5growth/5gr-ci& -b $GIT_CI clone https://github.com/5growth/5gr-ci&g" $file
done
cd 5gr-ci/minikube/local
kubectl apply -f monitoring_platform.yaml
kubectl apply -f so.yaml
kubectl apply -f vs.yaml
PROJ_ID=$(curl 10.168.123.10:8088)
sed -i "s/project_to_replace/${PROJ_ID}/g" rl.yaml
kubectl apply -f rl.yaml
