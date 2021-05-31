Described environment is made in order to propose an automated way to deploy 5Growth platform locally (on a working computer or personal laptop) in its current state for development and testing purposes.

This environment  includes:

*   5growth platform deployed on minikube;
*   Openstack cloud for workloads (devstack);
*   The supporting node for building, storing docker images, and cloudify.

Developer’s environment architecture described on picture 1:
<p align="center">
<img src="img/dev%20env.png" />
</p>

Presented environment allows developers to deploy a local lab, including 5growth platform and controlled via 5growth platform devstack cloud.

Lab is virtualized via VirtualBox, enveloped by a vagrant. Deployment consists of 3 VMs:

*   Node img is used as a private docker registry to store images required for 5growth platform deployment. Building 5growth platform components also happens here;
*   Devstack cloud is deployed on devstack node;
*   Minikube is deployed on the minikube node. Minikube deployment is based on driver “none”, which means that payload, i.e. containers, is on the same host as master. In other words - no nested virtualization needed. This approach simplifies architecture, saves host resources and allows streamline debugging.

**To start deployment it is required:**

1. Install VirtualBox

VirtualBox can be found here: [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)

<table>
  <tr>
   <td><strong>Ubuntu installation</strong>
   </td>
   <td><strong>CentOS installation</strong>
   </td>
   <td><strong>MacOS and windows</strong>
   </td>
  </tr>
  <tr>
   <td>Add repository key: \
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
<p>
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -
<p>
Add repository key:
<p>
sudo add-apt-repository "deb http://download.virtualbox.org/virtualbox/debian bionic contrib"
<p>
sudo apt-get update
<p>
Installation
<p>
sudo apt-get install virtualbox-6.1
   </td>
   <td>sudo yum install  -y elfutils elfutils-libelf-devel
<p>
sudo yum install -y patch gcc kernel-headers kernel-devel make perl wget
<p>
sudo wget http://download.virtualbox.org/virtualbox/rpm/el/virtualbox.repo -P /etc/yum.repos.d
<p>
sudo yum install VirtualBox-6.1
   </td>
   <td>Use the following link: <a href="https://www.virtualbox.org/wiki/Downloads">https://www.virtualbox.org/wiki/Downloads</a>

<p>
**Please NOTE!**

*For MacOS choose VirtualBox-5.2*
   </td>
  </tr>
</table>

2. Install Vagrant

Vagrant can be found here: [Vagrant](https://www.vagrantup.com/downloads.html)

3. Install vagrant plugins:

```
vagrant plugin install vagrant-vbguest vagrant-scp
```

4. Create network in virtualbox CLI:

```
VBoxManage natnetwork add --netname 5gnat --network "10.11.2.0/24" --enable --dhcp on
```

5. Clone 5growth CI repository

<!--git clone https://5growth.eu/git/5growth.5gr-ci -->
```
https://github.com/5growth/5gr-ci
```

6. Change to directory 5growth.5gr-ci/minikube/vagrant

```
cd 5growth.5gr-ci/minikube/vagrant

```

7. Run vagrant

```
vagrant box add generic/ubuntu1804 --provider virtualbox

vagrant up

```

**Please NOTE!**

*Execution vagrant up on windows may require that to run git-bash tool as administrator*

8. Wait till vagrant finished:

Vagrant starts VMs, deploys and configures software (it takes approximately from 40 minutes to 1.5 hour).

9. Access any node or service according to table:

Table 1. Nodes and services access

<table>
  <tr>
   <td><strong>Node or service name</strong>
   </td>
   <td><strong>Access URL</strong>
   </td>
   <td><strong>Login </strong>
   </td>
   <td><strong>Password </strong>
   </td>
   <td><strong>Notes </strong>
   </td>
  </tr>
  <tr>
   <td rowspan="2" >Img node
   </td>
   <td>ssh vagrant@10.168.123.11
   </td>
   <td>-
   </td>
   <td>vagrant
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>vagrant ssh img
   </td>
   <td>-
   </td>
   <td>-
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td rowspan="2" >minikube node
   </td>
   <td> ssh vagrant@10.168.123.9
   </td>
   <td>-
   </td>
   <td>vagrant
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>vagrant ssh minikube
   </td>
   <td>-
   </td>
   <td>-
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td rowspan="2" >Devstack node
   </td>
   <td> ssh vagrant@10.168.123.10
   </td>
   <td>-
   </td>
   <td>vagrant
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>vagrant ssh minikube
   </td>
   <td>-
   </td>
   <td>-
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>Devstack dashboard
   </td>
   <td><a href="http://10.168.123.10">http://10.168.123.10</a>
   </td>
   <td>admin
   </td>
   <td>admin
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>minikube
   </td>
   <td>Access from root user on minikube node
   </td>
   <td>
   </td>
   <td>
   </td>
   <td>Manifest is in folder:

<p>
/home/vagrant/scripts/5growth.5gr-ci
   </td>
  </tr>
  <tr>
   <td>5Gr-VS
   </td>
   <td>10.168.123.9/sebastian_web_gui/index.html
   </td>
   <td>admin
   </td>
   <td>admin
   </td>
   <td>
   </td>
  </tr>
  <tr>
   <td>5Gr-SO  
   </td>
   <td>http://10.168.123.9:8080/
   </td>
   <td>-
   </td>
   <td>-
   </td>
   <td>Register new user
   </td>
  </tr>
  <tr>
   <td>5Gr-RL
   </td>
   <td>http://10.168.123.9:50000
   </td>
   <td colspan="2" >No web interface
   </td>
   <td>
   </td>
  </tr>
</table>

**System requirements**

*   Virtualization support;
*   Minimum RAM amount 16GB;
*   Minimum disk space 30GB.

To tune RAM and CPU amount it is required to change correspondent value in the 5growth.5gr-ci/minikube/vagrant/Vagrantfile:

For tuning RAM amount please find and change row:

```
vb.memory =
```

For tuning CPU amount please find and change row:

```
vb.cpus =
```

**Environment description:**

Lab’s infra is described in the Vagrantfile. It includes  3 described nodes, each node has:

*   Reference to ubuntu image;
*   Hostname;
*   Additional NICs, connected to virtualBox host-only network with the specified IP (NAT is default);
*   Hosts file configuration;
*   Bootstrap file reference. Bootstrap file contains script, that deploy and configure software;
*   Specifies allocated RAM.

Vagrant file instantiate nodes consequentially. First instantiates the img node. Bootstrap script of img node is to:

*   Creates debug user (user name: user, password: passw0rd), which gives opportunity to ssh with password and access node through virtualBox console;
*   Installs docker and docker-compose;
*   Deploys and configures private registry;
*   Clone 5growth CI/CD repository;
*   Build and containerized 5growth components
*   Push builded images.

Bootstrap script of devstack node is to:

*   Creates debug user (user name: user, password: passw0rd), which gives opportunity to ssh with password and access node through virtualBox console;
*   Installs prerequisites and makes required configurations;
*   Creates local.conf file;
*   Installs devstack according to local.conf file
*   Pass OpenStack credentials to 5grows RL.

Bootstrap script of minikube node is to:
*   Creates debug user (user name: user, password: passw0rd), which gives opportunity to ssh with password and access node through virtualBox console;
*   Installing minikube and it’s prerequisites;
*   Configures docker to use private registry;
*   Deploys 5growth platform manifests using private registry and devstack credentials.