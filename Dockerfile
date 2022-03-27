FROM python:alpine

RUN apk update && apk upgrade
COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt gunicorn

COPY ./ /code/
WORKDIR /code/
ENV PYTHONPATH /code

ENV GUNICORN_CMD_ARGS "--bind=0.0.0.0:8000 --workers=2 --thread=4 --worker-class=gthread --forwarded-allow-ips='*' --access-logfile -"

CMD ["gunicorn", "app:app"]
