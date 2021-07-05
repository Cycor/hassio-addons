ARG BUILD_FROM
#FROM $BUILD_FROM
FROM homeassistant/aarch64-base:latest

ENV LANG C.UTF-8


RUN apk add --no-cache curl git build-base gcc wget cmake jq mosquitto-clients make python3 py3-pip && pip3 install mpp-solar

#RUN apt update && apt install -y curl git build-essential cmake jq mosquitto-clients

WORKDIR /opt

COPY sources/ /opt/
COPY run.sh /

RUN chmod a+x /run.sh

RUN cd /opt/inverter-cli && mkdir bin && cmake . && make && mv inverter_poller bin/

HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=1m \
    --retries=3 \
  CMD /opt/healthcheck

CMD [ "/run.sh" ]