FROM python:3.7

RUN mkdir -p /app /model

ENV ANALYTIC_PORT 45001
ENV MODEL_PATH /app/model/en-events.model

WORKDIR /app

RUN set -ex \
        # Install General Build Dependencies
        && apt-get update -qq -y --no-install-recommends \
        && apt-get upgrade -y --no-install-recommends \
        # Install the Python dependencies
        && cd /app

# Don't need this until requirements.txt read in, so move down for caching
ADD . /app/

RUN sh dependencies.sh \
        # Delete build dependencies
        && rm -rf /tmp/* \
        && apt-get autoremove -y \
        && apt-get purge -y \
        && apt-get clean -y \
        && rm -rf /var/lib/apt/lists/*

EXPOSE $ANALYTIC_PORT

CMD ["/app/launch.sh"]
