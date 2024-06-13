ARG VARIANT="3.12"
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

RUN apt update \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /tmp \
    && dpkg -i /tmp/google-chrome-stable_current_amd64.deb || true \
    && rm /tmp/google-chrome-stable_current_amd64.deb \
    && apt -y --fix-broken install \
    && apt clean \
    && pip install selenium webdriver-manager

COPY bot.py config.py .env /usr/src/app/
COPY handlers /usr/src/app/handlers
COPY filters /usr/src/app/filters
COPY keyboards /usr/src/app/keyboards
COPY middlewares /usr/src/app/middlewares
COPY models /usr/src/app/models
COPY utils /usr/src/app/utils

WORKDIR /usr/src/app/
CMD python3 bot.py