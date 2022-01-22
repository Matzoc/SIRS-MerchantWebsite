FROM mysql:5.7
WORKDIR /setup
USER root
COPY setup.sql setup.sql
#RUN mysql -p test -u root --password=password < setup.sql