#!/bin/bash

echo 'Starting SO starting'
python3 -m swagger_server &
echo 'Started SO started'
cd ../../ewbi/python-flask-server
python3 -m swagger_server
echo 'Starting SO EWBI started'

