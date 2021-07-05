# Cycor's hassio addons


## Installation

For installation read [the official instructions](https://www.home-assistant.io/hassio/installing_third_party_addons/) on the Home Assistant website and use github url :

```txt
https://github.com/Cycor/hassio-addons
```

## My addons


### voltronic-mqtt-v2

Based on docker-voltronic-homeassistant
- Uses mpp-solar to send commands, support for more devices
- Home assistant integration with unique id/availability
- Json payload

### smtptomqtt

- Receive emails on port 1025 and publish to MQTT.

### smtp_to_telegram

Source from kostyaesmukov/smtp_to_telegram
Modified to limit message length to 500 characters

- Receive emails on port 2525 and send to telegram.
