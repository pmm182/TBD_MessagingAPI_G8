FROM python:3.8

ARG APP_USER=tbd8
ARG APP_DIR=/opt/tbd/src

ENV UWSGI_PROCESSES_COUNT 20
ENV ENVIRONMENT "DOCKER"

RUN apt update \
    && apt upgrade -y \
    && rm -rf /var/lib/apt/lists/*
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
COPY --chown=${APP_USER}:${APP_USER} ./src ${APP_DIR}

WORKDIR ${APP_DIR}
USER ${APP_USER}

CMD ["sh", "-c", "uwsgi --socket 0.0.0.0:8080 --protocol http -w wsgi:app --lazy-apps --processes $UWSGI_PROCESSES_COUNT --master"]
EXPOSE 8080