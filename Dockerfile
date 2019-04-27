FROM alpine

LABEL maintainer="Zhiyuan Chen <zc@int.ac.cn>"

ENV HHD=/usr/local/hdd
RUN mkdir HHD
COPY src HHD
WORKDIR $HHD/src

RUN apk add --update python3
RUN pip3 install itchat

