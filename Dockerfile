FROM python:3.9.16

WORKDIR /app
ARG TARGET_BRANCH
ARG PIPELINES_MODEL
ENV DEPLOYMENT=local

RUN apt-get update \
&& apt-get -y install git \
&& git clone https://github.com/toposoid/toposoid-sentence-parser-english-web.git \
&& cd toposoid-sentence-parser-english-web \
&& git fetch origin ${TARGET_BRANCH} \
&& git checkout ${TARGET_BRANCH} \
&& pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
&& python -m spacy download ${PIPELINES_MODEL}



COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
