FROM joyzoursky/python-chromedriver:3.9-alpine-selenium
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt --no-cache-dir
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"
