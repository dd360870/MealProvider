FROM python

ARG DEBIAN_FRONTEND=noninteractive
ARG PIP_ROOT_USER_ACTION=ignore

RUN apt update && apt install -y mariadb-client

COPY . /app

WORKDIR /app

RUN pip install -e .

RUN useradd -ms /bin/bash nol

USER nol

CMD [ "/bin/bash", "-c", "gunicorn -b 0.0.0.0 -w 4 'flaskr:create_app()'" ]
