FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN pip3 install pika
RUN pip3 install pymongo

WORKDIR /database

COPY . /database

ENV PYTHONUNBUFFERED=0

CMD [ "python3", "-u", "database.py" ]
