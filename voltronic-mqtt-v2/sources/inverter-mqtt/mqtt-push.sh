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

bashio::log.info "Updating Status"

pushMQTTData () {
	local data="$1"

	mosquitto_pub \
		-h $MQTT_SERVER \
		-p $MQTT_PORT \
		-u "$MQTT_USERNAME" \
		-P "$MQTT_PASSWORD" \
		-t "$MQTT_TOPIC/$INV_DEVICENAME_CLEANED/state" \
		-m "$data"

	if [ "$DEBUG" = "true" ]; then
		bashio::log.info "$data"
	fi
}

cd /opt/inverter-cli/bin/
INVERTER_JSON_DATA=`timeout 10 /opt/inverter-cli/bin/inverter_poller -1`


pushMQTTData "$INVERTER_JSON_DATA"
