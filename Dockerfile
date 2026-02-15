FROM python:3.10

WORKDIR /app
ARG TARGET_BRANCH
ARG PIPELINES_MODEL
ENV DEPLOYMENT=local

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
&& apt-get -y install git unzip \
&& curl -LsSf https://astral.sh/uv/install.sh | sh \
&& source ${HOME}/.local/bin/env \
&& git clone https://github.com/toposoid/toposoid-sentence-parser-english-web.git \
&& cd toposoid-sentence-parser-english-web \
&& git fetch origin ${TARGET_BRANCH} \
&& git checkout ${TARGET_BRANCH} \
&& sed s/__##GIT_BRANCH##__/${TARGET_BRANCH}/g pyproject.toml.template > pyproject.toml \
&& uv sync \
&& uv add git+https://github.com/toposoid/toposoid-python-lib.git@${TARGET_BRANCH}#egg=ToposoidCommon \
&& uv run -- spacy download ${PIPELINES_MODEL}


COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
