FROM python:3.9-alpine
MAINTAINER Dillon Montag

# Does not allow python to buffer outputs, good for running Python within a Docker container
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt    # the "-r" flag is used to install from a requirements file

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# if you don't do this, the image runs the application using the root account
# don't want to give root access to an attacker in the docker container
RUN adduser -D user  # the "-D" flag means this user can only run applications
USER user
