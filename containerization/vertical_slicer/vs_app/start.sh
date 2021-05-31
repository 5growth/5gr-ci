#!/bin/bash

service apache2 start

echo 'Starting supervisor'
#java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 -jar Sebastian-0.0.2-SNAPSHOT.jar &
java -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 -jar SebastianCore-0.0.2-SNAPSHOT.jar &
exec supervisord -n


