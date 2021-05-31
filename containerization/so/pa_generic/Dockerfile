FROM python:2.7

RUN apt-get update

RUN mkdir -p /PA

COPY so_git/pa/genetic_algorithm/R1 /PA

WORKDIR /PA

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/PA"

EXPOSE 6161

ENTRYPOINT ["python"]

CMD ["ga_frontend.py", "-c", "settings.conf"]
