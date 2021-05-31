#!/bin/bash

apt-get install openvswitch-switch

ovs-vsctl add-br br0
ovs-vsctl add-br br1

ovs-vsctl add-port br0 ens7
ovs-vsctl add-port br1 ens9

ovs-vsctl set-controller br0 tcp:172.18.204.81:6653
ovs-vsctl set-controller br1 tcp:172.18.204.81:6653

ifconfig ens7 up
ifconfig ens9 up

ifconfig br0 192.168.1.208 netmask 255.255.255.0
ifconfig br1 192.168.1.208 netmask 255.255.255.0

