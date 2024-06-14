FROM python:3.12.4-alpine3.20

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update
RUN apk add chromium
RUN apk add chromium-chromedriver

ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip3 install --upgrade pip
RUN pip3 install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt --no-cache-dir
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}" 
