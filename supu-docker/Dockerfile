
FROM ubuntu:20.04
USER root

RUN apt update
RUN apt install -y python3.9
RUN apt install -y python3-pip

COPY requirements.txt .
RUN python3.9 -m pip install -r requirements.txt 

ENV SITE_DOMAIN=vtuber.supu.com

WORKDIR /var

ADD https://archive.ics.uci.edu/static/public/53/iris.zip .

COPY scripty.py .

ENTRYPOINT ["python3.9", "scripty.py"]