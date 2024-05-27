FROM python

ARG DEBIAN_FRONTEND=noninteractive
ARG PIP_ROOT_USER_ACTION=ignore

RUN apt update && apt install -y mariadb-client

RUN useradd -ms /bin/bash nol

USER nol

WORKDIR /app

COPY ./pyproject.toml ./pyproject.toml
COPY ./flaskr ./flaskr
COPY ./data.sql ./data.sql

USER root
RUN pip install -e .

USER nol

#CMD [ "/bin/bash", "-c", "gunicorn -b 0.0.0.0:8000 -w 4 'flaskr:create_app()'" ]
CMD [ "/bin/bash", "-c", "flask --app flaskr run --host 0.0.0.0 --port 8000" ]