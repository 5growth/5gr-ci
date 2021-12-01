#!/bin/bash
sudo docker exec cfy_mano_local bash -c "until cfy plugins upload http://repository.cloudifysource.org/cloudify/wagons/cloudify-openstack-plugin/2.14.7/cloudify_openstack_plugin-2.14.7-py27-none-linux_x86_64-centos-Core.wgn -y http://www.getcloudify.org/spec/openstack-plugin/2.14.7/plugin.yaml; do echo nicht; done"
sudo docker exec cfy_mano_local bash -c "until cfy plugins upload /home/centos/cloudify_mtp_plugin-0.0.1-centos-Core-py27.py36-none-linux_x86_64.wgn -y /home/centos/plugin.yaml; do echo nicht; done"
