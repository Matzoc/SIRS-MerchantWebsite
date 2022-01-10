# syntax=docker/dockerfile:1
FROM ubuntu
WORKDIR /code
ENV FLASK_APP=__init__.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt-get update
RUN apt-get install mysql-client -y
RUN apt-get install libmysqlclient-dev mysql-server -y
RUN apt-get install pip -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]