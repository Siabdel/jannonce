FROM python:3.8.3-slim
#FROM debian-debian-bullseye-slim

ENV PYTHONDONTWRITEBYTECODE 1 ## demande a django ne pas generer de fichier pyc
ENV PYTHONUNBUFFERED 1

# copy source and install dependencies
WORKDIR /code/markoblog/
RUN mkdir -p /opt/app/pip_cache

COPY requirements.txt /code/
COPY .env /code/
COPY markoblog /code/markoblog/
COPY entrypoint.sh /code/markoblog/entrypoint.sh


RUN pip install --upgrade pip

# install psycopg2
RUN apt update
RUN apt install gcc python3-dev -y
##
RUN apt install python3-pip -y
RUN pip install --upgrade pip
##RUN pip3 install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN pip3 install -r requirements.txt

RUN chmod 777 /code/markoblog/entrypoint.sh
RUN ls -l /code/markoblog/entrypoint.sh

WORKDIR /code/markoblog

# run entrypoint.sh
## this is oddly named. Entrypoints should use ENTRYPOINT not CMD
## recommend renaming this to make it clear what it's used for
## If it's a long running service, it shouldn't use a shell script
CMD ["./entrypoint.sh"]
