# pull official base image
FROM python:3.6.10-alpine3.9

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . /usr/src/app/

# install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc libxslt-dev python3-dev musl-dev && \
    apk add postgresql-dev

RUN pip3 install -r requirements.txt

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
