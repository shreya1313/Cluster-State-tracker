FROM spotmentor/alpine-protobuf:1.0.0

RUN apk add --no-cache --virtual .build-deps build-base

RUN apk add --no-cache --virtual .run-deps git

ENV PYTHONUNBUFFERED 1

ENV LIBRARY_PATH=/lib:/usr/lib

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt && apk del .build-deps

ADD src/ /code/

RUN adduser -D -u 1001 -g 1001 celery

ENTRYPOINT ["/code/common/startup.sh"]
