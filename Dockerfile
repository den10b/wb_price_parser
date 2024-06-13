FROM joyzoursky/python-chromedriver:3.9-alpine-selenium
# Update the package lists
RUN apk del python3

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
# Verify the installation
RUN python3 --version

ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt --no-cache-dir
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"
