# smtptomqtt

Receive emails on port 1025 and publish to MQTT. Topic will be `<configurable_prefix>/<sender_email.replace('@', '_')>`.

It's based on aiosmtpd and paho-mqtt.

## Run it

1. Update settings
2. Go.