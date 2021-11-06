FROM python:3.8

ARG APP_USER=tbd8
ARG APP_DIR=/opt/tbd/src

ENV APP_DIR=${APP_DIR}
ENV UWSGI_PROCESSES_COUNT 20
ENV UWSGI_THREADS_COUNT 25

ENV ENVIRONMENT "ATLAS"
ENV MONGODB_USERNAME ""
ENV MONGODB_PASSWORD ""
ENV MONGODB_SERVER ""

RUN apt update \
    && apt upgrade -y \
    && rm -rf /var/lib/apt/lists/*
RUN curl -o /tmp/mongo_tools.deb https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2004-x86_64-100.5.1.deb \
    && dpkg -i /tmp/mongo_tools.deb
RUN curl -o /tmp/mongosh.deb https://downloads.mongodb.com/compass/mongodb-mongosh_1.1.2_amd64.deb \
    && dpkg -i /tmp/mongosh.deb
RUN groupadd ${APP_USER} --gid 2000 \
    && useradd ${APP_USER} --gid 2000 \
        --create-home \
        --gid 2000 \
        --shell /bin/bash \
        --uid 2000 \
        --no-log-init \
    && mkdir -p ${APP_DIR} \
    && chown -R ${APP_USER}.${APP_USER} ${APP_DIR} \
    && passwd -l ${APP_USER}

COPY ./requirements.txt ${APP_DIR}/requirements.txt
RUN pip install -r ${APP_DIR}/requirements.txt
COPY ./start.sh ${APP_DIR}/start.sh
COPY --chown=${APP_USER}:${APP_USER} ./src ${APP_DIR}

WORKDIR ${APP_DIR}
USER ${APP_USER}

CMD ["sh", "-c", "${APP_DIR}/start.sh"]
EXPOSE 8080