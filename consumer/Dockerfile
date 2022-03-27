FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN pip3 install pika

WORKDIR /consumer

COPY . /consumer

ENTRYPOINT [ "python3" ]

CMD [ "consumer.py" ]
