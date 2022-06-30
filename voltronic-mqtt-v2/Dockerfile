ARG BUILD_FROM
FROM $BUILD_FROM

ENV \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add --no-cache mosquitto-clients py3-pip && pip3 install mpp-solar paho-mqtt

WORKDIR /opt

COPY sources/ /opt/
COPY run.sh /

HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=1m \
    --retries=3 \
  CMD /opt/healthcheck

RUN chmod a+x /run.sh
RUN chmod a+x -R /opt

CMD [ "/run.sh" ]