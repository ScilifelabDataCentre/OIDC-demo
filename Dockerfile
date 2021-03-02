FROM python:3.8-alpine

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev rust cargo

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt
RUN pip3 install gunicorn

COPY ./ /code/
WORKDIR /code/
ENV PYTHONPATH /code

ENV GUNICORN_CMD_ARGS "--bind=0.0.0.0:8000 --workers=2 --thread=4 --worker-class=gthread --forwarded-allow-ips='*' --access-logfile -"

CMD ["gunicorn", "app:app"]
