FROM python:3.8.3-slim
#FROM debian:bullseye-slim

ENV PYTHONDONTWRITEBYTECODE 1 ## demande a django ne pas generer de fichier pyc
ENV PYTHONUNBUFFERED 1
# copy source and install dependencies
WORKDIR /app
RUN mkdir -p /opt/app/pip_cache

COPY requirements.txt /app/
COPY .env /app/
COPY . /app/jannonce/
COPY entrypoint.sh /app/jannonce/entrypoint.sh

# install psycopg2
# RUN apt update && apt upgrade && apt autoclea
RUN apt update

RUN apt install -y gcc python3-dev libpq-dev python3-pip wget curl vim 
#RUM apt install -y python-dev python-pip python-imaging libmagickwand-devpillow libjpeg-dev 
RUN apt install -y git nodejs npm postgresql-client redis-server wkhtmltopdf
RUN apt install -y curl vim tree fabric openssh-server
RUN apt install -y libssl-dev build-essential libffi-dev
RUN apt clean
##
#
RUN pip install --upgrade pip
RUN ls -l /app/
RUN chmod 777 /app/requirements.txt
RUN pip3 install -r /app/requirements.txt --cache-dir /opt/app/pip_cache
RUN pip3 install django
RUN pip3 install psycopg2-binary

RUN chmod a+x /app/jannonce/entrypoint.sh

WORKDIR /app/jannonce

# run entrypoint.sh
## this is oddly named. Entrypoints should use ENTRYPOINT not CMD
## recommend renaming this to make it clear what it's used for
## If it's a long running service, it shouldn't use a shell script
CMD ["./entrypoint.sh"]
