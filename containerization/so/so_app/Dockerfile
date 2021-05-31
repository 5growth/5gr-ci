FROM python:3.6

RUN apt-get update
RUN apt-get install -y python-dev libcurl4-gnutls-dev gcc
RUN apt-get install -y libgnutls28-dev
RUN pip install pyyaml
RUN pip install pycurl

RUN mkdir -p /usr/src/app/5Gr-SO

COPY so_git/5Gr-SO /usr/src/app/5Gr-SO
COPY so_app/start.sh /usr/src/app/5Gr-SO/nbi/python-flask-server/start.sh

WORKDIR /usr/src/app/5Gr-SO/coreMano/osmclient/

RUN python3 setup.py install

WORKDIR /usr/src/app/5Gr-SO
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/5Gr-SO/nbi/python-flask-server
RUN pip3 install --no-cache-dir -r requirements.txt

#RUN sed -i 's/db.ip.*/db.ip=so_mongo/g' /usr/src/app/5Gr-SO/db/db.properties

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/5Gr-SO:/usr/src/app/5Gr-SO/sm:/usr/src/app/5Gr-SO/nbi:/usr/src/app/5Gr-SO/db:/usr/src/app/5Gr-SO/coreMano:/usr/src/app/5Gr-SO/log:/usr/src/app/5Gr-SO/nbi/python-flask-server"

EXPOSE 8080
EXPOSE 8085

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]