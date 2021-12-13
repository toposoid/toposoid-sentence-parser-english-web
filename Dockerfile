FROM python:3.9-alpine

WORKDIR /app
ARG TARGET_BRANCH
ENV DEPLOYMENT=local

RUN apk add --no-cache build-base \
&& pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
&& apk del build-base \
&& git clone https://github.com/toposoid/toposoid-sentence-parser-english-web.git \
&& cd toposoid-sentence-parser-english-web \
&& git fetch origin ${TARGET_BRANCH} \
&& git checkout ${TARGET_BRANCH} 

COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
