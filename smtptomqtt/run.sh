#!/usr/bin/env bashio

export MQTT_HOST="$(bashio::config 'MqttHost')"
export MQTT_PORT="$(bashio::config 'MqttPort')"
export MQTT_USERNAME="$(bashio::config 'MqttUsername')"
export MQTT_PASSWORD="$(bashio::config 'MqttPassword')"
export MQTT_TOPIC="$(bashio::config 'MqttTopic')"
export DEBUG="$(bashio::config 'Debug')"
	
python3 smtptomqtt.py