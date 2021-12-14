FROM python:3.9-alpine

WORKDIR /app
ARG TARGET_BRANCH
ENV DEPLOYMENT=local

RUN apk add --no-cache build-base cargo git \
&& git clone https://github.com/toposoid/toposoid-sentence-parser-english-web.git \
&& cd toposoid-sentence-parser-english-web \
&& git fetch origin ${TARGET_BRANCH} \
&& git checkout ${TARGET_BRANCH} \
&& pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
&& python -m spacy download en_core_web_lg \
&& apk del build-base


COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
