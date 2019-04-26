FROM python:3.6-alpine

LABEL maintainer="Zhiyuan Chen <zc@int.ac.cn>"

ENV HHD=/usr/local/hdd
RUN mkdir HHD
COPY src HHD
WORKDIR $HHD/src

RUN apk add --no-cache gcc musl-dev
RUN pip install itchat

ENTRYPOINT ["bash", "-c", "python $HHD/src/main.py"]
