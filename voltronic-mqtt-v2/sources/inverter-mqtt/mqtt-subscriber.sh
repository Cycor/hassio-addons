#!/usr/bin/env bashio

INV_PORT="$(bashio::config 'InverterPort')"
INV_MANUFACTURER="$(bashio::config 'InverterManufacturer')"
INV_DEVICENAME="$(bashio::config 'InverterName')"

MQTT_SERVER="$(bashio::config 'MqttHost')"
MQTT_PORT="$(bashio::config 'MqttPort')"
MQTT_TOPIC="$(bashio::config 'MqttTopic')"
MQTT_USERNAME="$(bashio::config 'MqttUsername')"
MQTT_PASSWORD="$(bashio::config 'MqttPassword')"
MQTT_HATOPIC="$(bashio::config 'haTopic')"
DEBUG="$(bashio::config 'debug')"

TMP=${INV_DEVICENAME// /_}
INV_DEVICENAME_CLEANED=${TMP,,}

bashio::log.info "Listening on $MQTT_TOPIC/$INV_DEVICENAME_CLEANED/cmd"

while read rawcmd;
do

    bashio::log.info "Incoming request send: [$rawcmd] to inverter."

    #/opt/inverter-cli/bin/inverter_poller -r $rawcmd;
	mpp-solar -p $INV_PORT -c $rawcmd


done < <(mosquitto_sub -h $MQTT_SERVER -p $MQTT_PORT -u "$MQTT_USERNAME" -P "$MQTT_PASSWORD" -t "$MQTT_TOPIC/$INV_DEVICENAME_CLEANED/cmd" --will-topic "$MQTT_TOPIC/$INV_DEVICENAME_CLEANED/status" --will-payload "Offline" --will-retain -q 1)

bashio::log.info "Listener closed"