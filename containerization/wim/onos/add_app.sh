#!/bin/bash

host=127.0.0.1

apps[0]="org.onosproject.drivers"
apps[1]="org.onosproject.hostprovider"
apps[2]="org.onosproject.lldpprovider"
apps[3]="org.onosproject.gui"
apps[4]="org.onosproject.openflow-base"
apps[5]="org.onosproject.openflow"
apps[6]="org.onosproject.optical-model"
apps[7]="org.onosproject.proxyarp"

for item in ${apps[*]}
do
    until
    curl -X POST \
      http://$host:8181/onos/v1/applications/$item/active \
      -H 'Accept: */*' \
      -H 'Authorization: Basic b25vczpyb2Nrcw==';
      do
          echo "Waiting for ONOS"
            sleep 2
      done
done

