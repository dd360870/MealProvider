FROM python

ENV TZ="Asia/Taipei"

ARG DEBIAN_FRONTEND=noninteractive
ARG PIP_ROOT_USER_ACTION=ignore

RUN apt update && apt install -y mariadb-client

RUN useradd -ms /bin/bash nol

USER nol

WORKDIR /app

COPY ./pyproject.toml ./pyproject.toml
COPY ./flaskr ./flaskr
COPY ./data.sql ./data.sql
COPY ./make_celery.py ./make_celery.py

USER root
RUN pip install -e .

USER nol

CMD [ "/bin/bash", "-c", "gunicorn -b 0.0.0.0:8000 -w 1 --access-logfile - --capture-output --error-logfile - --log-level INFO 'flaskr:create_app()'" ]
