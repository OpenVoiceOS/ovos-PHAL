FROM debian:buster-slim

ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
  apt-get install -y git python3 python3-dev python3-pip curl build-essential && \
  c_rehash && \
  apt-get autoremove -y && \
  apt-get clean && \
  useradd --no-log-init mycroft -m

# the lines above are kept static so that docker layer is shared and cached among all containers

COPY . /tmp/ovos-phal
RUN pip3 install /tmp/ovos-phal

# TODO remove this, missing dependency in ovos-core
RUN pip3 install pyee==8.1.0 ovos-utils==0.0.21a2

USER mycroft
ENTRYPOINT ovos_PHAL