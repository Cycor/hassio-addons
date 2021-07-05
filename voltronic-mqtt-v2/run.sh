#!/usr/bin/env bashio

bashio::log.info "Here we go"

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


echo "INV_PORT=$INV_PORT"
echo "INV_MANUFACTURER=$INV_MANUFACTURER"
echo "INV_DEVICENAME=$INV_DEVICENAME"
echo "MQTT_SERVER=$MQTT_SERVER"
echo "MQTT_PORT=$MQTT_PORT"
echo "MQTT_TOPIC=$MQTT_TOPIC"
echo "MQTT_USERNAME=$MQTT_USERNAME"
echo "MQTT_PASSWORD=$MQTT_PASSWORD"
echo "MQTT_HATOPIC=$MQTT_HATOPIC"
echo "DEBUG=$DEBUG"

cp /opt/inverter-cli/inverter.conf /opt/inverter-cli/bin/inverter.conf
sed -i "s/^\(device=\).*/\1${INV_PORT//\//\\/}/" /opt/inverter-cli/bin/inverter.conf

cd /opt
/opt/inverter-mqtt/entrypoint.sh