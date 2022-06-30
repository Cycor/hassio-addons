#!/usr/bin/env bashio

export TERM=xterm

INV_DEVICENAME="$(bashio::config 'InverterName')"
TMP=${INV_DEVICENAME// /_}
INV_DEVICENAME_CLEANED=${TMP,,}
export INV_DEVICENAME_CLEANED=$INV_DEVICENAME_CLEANED

bashio::log.info Starting Home Assistant mqtt script
python -u /opt/mqtt.py
