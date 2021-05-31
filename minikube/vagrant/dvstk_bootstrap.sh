#!/bin/bash
#exec 1 |tee log.log 2>&1
#set -x
echo "Creating debugging user with password Username: user, Password: passw0rd"
adduser --quiet --disabled-password --shell /bin/bash --home /home/user --gecos "User with password ssh auth" user
echo "user:passw0rd" | chpasswd
echo "user ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/user

echo "Updating system..."
sudo apt update							                         >> /dev/null 2>&1
sudo apt upgrade -y              			              >> /dev/null 2>&1
sudo apt install -y bridge-utils python-pip python3-pip               >> /dev/null 2>&1
sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-pil python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev               >> /dev/null 2>&1
pip install --upgrade pip                                                   >> /dev/null 2>&1
echo "net.ipv4.ip_forward=1" 		        	|sudo tee -a /etc/sysctl.conf
echo "net.ipv4.conf.default.rp_filter=0" 	|sudo tee -a /etc/sysctl.conf
echo "net.ipv4.conf.all.rp_filter=0" 	  	|sudo tee -a /etc/sysctl.conf
sysctl -p
echo "System updated"

echo "creating stack"
sudo useradd -s /bin/bash -d /opt/stack -m stack
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack

ip r del default via 10.0.2.2 dev eth0

myip=$(hostname -I | cut -d' ' -f3)
mygtw=$(ip route | awk '/default/ { print $3 }')
myrng=$(ip route | grep "src $myip" | awk '{print $1}' |  grep ".0/")

echo "creating local.conf"
cat << EOF > local.conf
[[local|localrc]]
RECLONE=yes
IP_VERSION=4
HOST_IP=${myip}

PUBLIC_INTERFACE=eth2

ADMIN_PASSWORD=admin
DATABASE_PASSWORD=\$ADMIN_PASSWORD
RABBIT_PASSWORD=\$ADMIN_PASSWORD
SERVICE_PASSWORD=\$ADMIN_PASSWORD

LIBVIRT_TYPE=kvm     # KVM

## Neutron options
Q_USE_PROVIDERNET_FOR_PUBLIC=True
OVS_PHYSICAL_BRIDGE=br-ex
PUBLIC_BRIDGE=br-ex
OVS_BRIDGE_MAPPINGS=public:br-ex
#Q_USE_PROVIDER_NETWORKING=True

## Neutron Networking options used to create Neutron Subnets
#IPV4_ADDRS_SAFE_TO_USE="${myrngnat}"
#NETWORK_GATEWAY=${mygtw}
#PROVIDER_SUBNET_NAME="provider_net"
#PROVIDER_NETWORK_TYPE="flat"
#USE_SUBNETPOOL=False      # external DHCP

#IPV4_ADDRS_SAFE_TO_USE="10.150.0.0/24"
#FIXED_RANGE=10.150.0.0/24
#SUBNETPOOL_PREFIX_V4="10.150.0.0/24"
#NETWORK_GATEWAY=10.150.0.1

FLOATING_RANGE="${myrng}"
PUBLIC_NETWORK_GATEWAY=${mygtw}
Q_FLOATING_ALLOCATION_POOL=start=10.11.2.100,end=10.11.2.200

#logging
LOGFILE=/opt/stack/devstack/logs/stack.sh.log
LOGDAYS=1
LOG_COLOR=True

DOWNLOAD_DEFAULT_IMAGES=False
IMAGE_URLS="https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img,"
IMAGE_URLS+="http://download.cirros-cloud.net/0.5.1/cirros-0.5.1-x86_64-disk.img,"
#IMAGE_URLS+="https://cloud-images.ubuntu.com/xenial/current/xenial-server-cloudimg-amd64-disk1.img,"
EOF

whoami
sudo -i -u stack bash << EOF
echo "In"
whoami
pip install jsonschema==3.2.0 >> /dev/null 2>&1
echo "Installing git..." && sudo apt -y install git >> /dev/null 2>&1
echo "Cloning..." && git clone -b stable/stein https://git.openstack.org/openstack-dev/devstack >> /dev/null 2>&1
EOF

whoami
sudo -i bash << EOF
echo "In"
whoami
cp /home/vagrant/local.conf /opt/stack/devstack/
chown stack:stack /opt/stack/devstack/local.conf
EOF
echo "Out"
whoami


whoami
sudo -i -u stack bash << EOF
echo "In"
whoami
cd devstack
./stack.sh
EOF
echo "Out"
whoami

whoami
sudo -i -u stack bash << EOF
echo "In"
whoami
cd devstack
echo "Additional configurations"
. openrc admin admin

until openstack network list ; do echo "Waiting for openstack CLI return"; sleep 2; done

#PRJ=$(openstack project list | grep admin | grep -v "_admin" | awk '{print $2}')
#echo $PRJ
#SECG=$(openstack security group list | grep $PRJ | awk '{print $2}')
#echo $SECG
#openstack security group rule create ${SECG} --protocol icmp
#openstack security group rule create  ${SECG} --protocol tcp --dst-port 22:22

openstack network create local
openstack subnet create local_sub --network local --subnet-range  192.168.150.0/24 --dhcp --ip-version 4 --allocation-pool start=192.168.150.2,end=192.168.150.250

openstack router create router
openstack router set router --external-gateway public
openstack router add subnet router local_sub

cat << ENF > openstack-key.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDjHIGG5t04MUlEcTX4V9J3JmmmdpGo6dE6D5PwB/YPzIgWuxhSzLQaD6LHk6RYmIUBvk8t05ObhuxJGej4PxWJRTTlDbXedC4CORsNByPAM6Uj75NBiaU+FdwNzxAsont6p3z3ko5I89bGYUOynCG2C5lBM2lmhA3r5xCJj8BwWSXKu3gXYeBgPWgx6ctTWlmaMldTBRcYhH7HjVh9OMo3DTRJ9hpJf+4rFxEDwH4jC7eR7GaV2ZDqsFmzRTeI2E0XYEgCB+gF4u3lPx29DFsVLp5ehVihMDsUNUYKM6UDW11h3pR94TN2gODwDBLUIxzO/i9ZubIZWz+DrlqQzZdH
ENF

openstack keypair create --public-key openstack-key.pub sssakey

FLAVORS=("flavor_spr1" "flavor_spr2" "flavor_webserver" "flavor_probeserver")
for FLAVOR in ${FLAVORS[@]}
do
openstack flavor create --vcpus 1 --ram 64 --disk 1 ${FLAVOR}
done
#openstack server create --image $(openstack image list | awk '/ cirros-.*-x86_64-.* / {print $2}') --flavor 1 --nic net-id=$(openstack network list | awk '/ local / {print $2}') node1

mysql keystone -uroot -padmin -D keystone -BNe "select id from project where name = 'admin';" > index.html
#screen -d -m bash -c 'python -m SimpleHTTPServer 8088'

cat << END > server.py
import sys
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer


def test(HandlerClass=SimpleHTTPRequestHandler,
         ServerClass=BaseHTTPServer.HTTPServer):

    protocol = "HTTP/1.0"
    host = ''
    port = 8000
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if ':' in arg:
            host, port = arg.split(':')
            port = int(port)
        else:
            try:
                port = int(sys.argv[1])
            except:
                host = sys.argv[1]

    server_address = (host, port)

    HandlerClass.protocol_version = protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()


if __name__ == "__main__":
    test()
END

screen -d -m bash -c 'python  server.py 10.168.123.10:8088'

PRJ=$(openstack project list | grep admin | grep -v "_admin" | awk '{print $2}')
echo $PRJ
SECG=$(openstack security group list | grep $PRJ | awk '{print $2}')
echo $SECG
echo "openstack security group rule create ${SECG} --protocol icmp"
openstack security group rule create  ${SECG} --protocol tcp --dst-port 22:22

EOF
echo "Out"
whoami