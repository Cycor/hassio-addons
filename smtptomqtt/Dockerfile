ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

WORKDIR /smtptomqtt

COPY run.sh smtptomqtt.py requirements.txt ./
RUN chmod a+x ./run.sh

RUN apk add --no-cache python3 py3-pip && pip3 install -r requirements.txt

CMD [ "./run.sh" ]


