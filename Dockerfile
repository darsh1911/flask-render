FROM ubuntu:latest
LABEL authors="darsh"

ENTRYPOINT ["top", "-b"]

RUN pip install -r requirements.txt
