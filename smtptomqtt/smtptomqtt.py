#!/usr/bin/env python3
import asyncio
import email
import logging
import os
import signal
import time
import json
import xml.etree.ElementTree
from datetime import datetime
from email.policy import default


from aiosmtpd.controller import Controller
from paho.mqtt import publish

defaults = {
    "SMTP_PORT": 1025,
    "MQTT_HOST": "localhost",
    "MQTT_PORT": 1883,
    "MQTT_USERNAME": "",
    "MQTT_PASSWORD": "",
    "MQTT_TOPIC": "smtptomqtt",
    "DEBUG": "False",
}
config = {
    setting: os.environ.get(setting, default) for setting, default in defaults.items()
}
# Boolify
for key, value in config.items():
    if value == "True":
        config[key] = True
    elif value == "False":
        config[key] = False

level = logging.DEBUG if config["DEBUG"] else logging.INFO

log = logging.getLogger("smtptomqtt")
log.setLevel(level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Log to console
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


class SMTPTOMQTTHandler:
    def __init__(self, loop):
        self.loop = loop
        self.quit = False
        signal.signal(signal.SIGTERM, self.set_quit)
        signal.signal(signal.SIGINT, self.set_quit)

    def remove_tags(self, text):
        return ''.join(xml.etree.ElementTree.fromstring(text).itertext())

    async def handle_DATA(self, server, session, envelope):
        log.debug("Message from %s", envelope.mail_from)
        msg = email.message_from_bytes(envelope.original_content, policy=default)
        
        mailFrom = msg['From'];
        mailTo = msg['To'];
        mailSubject = msg['Subject'];

        log.debug(
            "Message data (truncated): %s",
            envelope.content.decode("utf8", errors="replace")[:250],
        )
        
        mailContent = ''
        contenttype = None
        suffix = '' 
        for part in msg.walk():
            if not part.is_multipart():
                contenttype = part.get_content_type()
                filename = part.get_filename()
                charset = part.get_content_charset()
                if filename:     #is annex?
                    print(filename)
                else:
                    if charset == None:
                        mailContent = part.get_payload()
                    else:
                        mailContent = part.get_payload(decode=True).decode(charset)
                    if contenttype in ['text/plain']:
                        suffix = '.txt'
                    elif contenttype in ['text/html']:
                        suffix = '.htm'
                        mailContent = self.remove_tags(mailContent)
                     
        
        topic = "{}/{}".format(
            config["MQTT_TOPIC"], envelope.mail_from.replace("@", "_")
        )
        
        jsonStr = json.dumps({
          'from': mailFrom,
          'to': mailTo,
          'subject': mailSubject,
          'contents': mailContent.strip()
        })
        
        self.mqtt_publish(topic, jsonStr)
        
        for att in msg.iter_attachments():
            # Just save images
            if not att.get_content_type().startswith("image"):
                continue
                
            filename = att.get_filename()
            image_data = att.get_content()
            
            topic2 = "{}/{}/{}".format(
                config["MQTT_TOPIC"], envelope.mail_from.replace("@", ""), filename
            )
            
            log.info("Sending attached file %s", 
                topic2
            )
            self.mqtt_publish(topic2, image_data)

        return "250 Message accepted for delivery"

    def mqtt_publish(self, topic, payload):
        log.info('Publishing "%s" to %s', payload, topic)
        try:
            publish.single(
                topic,
                payload,
                hostname=config["MQTT_HOST"],
                port=int(config["MQTT_PORT"]),
                auth={
                    "username": config["MQTT_USERNAME"],
                    "password": config["MQTT_PASSWORD"],
                }
                if config["MQTT_USERNAME"]
                else None,
            )
        except Exception as e:
            log.exception("Failed publishing")

    def set_quit(self, *args):
        log.info("Quitting...")
        self.quit = True


if __name__ == "__main__":
    log.debug(", ".join([f"{k}={v}" for k, v in config.items()]))

    # If there's a dir called log - set up a filehandler
    if os.path.exists("log"):
        log.info("Setting up a filehandler")
        fh = logging.FileHandler("log/smtptomqtt.log")
        fh.setFormatter(formatter)
        log.addHandler(fh)

    loop = asyncio.get_event_loop()
    c = Controller(
        handler=SMTPTOMQTTHandler(loop),
        loop=loop,
        hostname="0.0.0.0",
        port=config["SMTP_PORT"],
    )
    c.start()
    log.info("Running")
    try:
        while not c.handler.quit:
            time.sleep(0.5)
        c.stop()
    except:
        c.stop()
        raise
