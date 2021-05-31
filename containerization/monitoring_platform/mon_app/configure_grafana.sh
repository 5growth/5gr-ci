#!/bin/bash
set -e

host="$1"
shift


until result=$(curl  --silent -X POST -H "Content-Type: application/json" -d '{"name":"apikeycurl", "role": "Admin"}' http://admin:admin@$host:3000/api/auth/keys); do
    echo "Waiting for Grafana"
    sleep 2
done
echo "Grafana is active"

if [[ $result == *"Failed"* ]];then
    echo "Key do not created($result)";
    exit 1
  else

    key=$(echo $result | grep key | awk -F '"' '{print $10}')
    cp config.properties config.propertiesnew
    sed -i "s/grafana\.token.*/grafana\.token=$key/" config.propertiesnew
    cp -f config.propertiesnew config.properties
    echo "Grafana key configurated in monitoring platform"
fi
java -jar target/configmanager-1.0.0-SNAPSHOT-fat.jar



