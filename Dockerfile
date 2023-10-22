# start with a base image
# FROM ubuntu:16.04
FROM python:3.7.2-slim

# set environment vars
ENV PYTHONPATH="app:${PYTHONPATH}"

USER root

# update stretch repositories
RUN sed -i s/deb.debian.org/archive.debian.org/g /etc/apt/sources.list
RUN sed -i 's|security.debian.org|archive.debian.org/|g' /etc/apt/sources.list
RUN sed -i '/stretch-updates/d' /etc/apt/sources.list

# install dependencies
RUN apt-get update && apt-get install -y \
apt-utils \
python3-pip \
libffi-dev \
&& rm -rf /var/lib/apt/lists/*


# update working directories
ADD ./short_url /short_url
ADD ./requirements /requirements
ADD ./requirements.txt /requirements.txt
ADD ./pre_script.sh /pre_script.sh
# install dependencies
RUN pip install --upgrade pip
RUN ls short_url 
RUN pip3 install -r requirements.txt

#RUN python short_url/script.py
RUN chmod 755 /pre_script.sh

CMD ["python3", "short_url/app.py"]