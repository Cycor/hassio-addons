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

#
# Simple script to register the MQTT topics when the container starts for the first time...

registerTopicToHA () {

	local name=$1
	local jsonKey=$2

	local tmp=${name// /_}
	local cleaned_up_name=${tmp,,}
	
	local unit_of_measurement=$3
	local icon=$4

    mosquitto_pub \
        -h $MQTT_SERVER \
        -p $MQTT_PORT \
        -u "$MQTT_USERNAME" \
        -P "$MQTT_PASSWORD" \
        -t "$MQTT_HATOPIC/sensor/"$INV_DEVICENAME_CLEANED"/$cleaned_up_name/config" \
		-r \
        -m "{
            \"name\": \"$INV_DEVICENAME $name\",
            \"unit_of_measurement\": \"$unit_of_measurement\",
            \"state_topic\": \"$MQTT_TOPIC/"$INV_DEVICENAME_CLEANED"/state\",
            \"value_template\": \"{{ $jsonKey }}\",
            \"icon\": \"mdi:$icon\",
            \"availability\": {
              \"topic\": \"$MQTT_TOPIC/"$INV_DEVICENAME_CLEANED"/status\",
              \"payload_available\": \"Online\",
              \"payload_not_available\": \"Offline\"
            },
            \"unique_id\":\""$INV_DEVICENAME_CLEANED"_$cleaned_up_name\",
            \"device\": {
              \"name\": \"$INV_DEVICENAME\",
              \"identifiers\": \"$INV_DEVICENAME_CLEANED\",
              \"manufacturer\": \"$INV_MANUFACTURER\"
            }
        }"
}

registerInverterRawCMDToHA () {
    mosquitto_pub \
        -h $MQTT_SERVER \
        -p $MQTT_PORT \
        -u "$MQTT_USERNAME" \
        -P "$MQTT_PASSWORD" \
        -t "$MQTT_HATOPIC/$INV_DEVICENAME_CLEANED/config" \
        -m "{
            \"name\": \"$INV_DEVICENAME\",
            \"state_topic\": \"$MQTT_TOPIC/$INV_DEVICENAME_CLEANED/cmd\"
            \"device\": {
              \"name\": \"$INV_DEVICENAME\",
              \"identifiers\": \"$INV_DEVICENAME_CLEANED\",
              \"manufacturer\": \"$INV_MANUFACTURER\"
            }			
        }"
}


registerTopicToHA "Inverter mode"				"value_json.Inverter_mode | int"						""		"solar-power" # 1 = Power On, 2 = Standby, 3 = Line, 4 = Battery, 5 = Fault, 6 = Power Saving, 7 = Unknown
registerTopicToHA "AC grid voltage"				"value_json.AC_grid_voltage | float"					"V"		"power-plug"
registerTopicToHA "AC grid frequency"			"value_json.AC_grid_frequency | float"					"Hz"	"current-ac"
registerTopicToHA "AC out voltage"				"value_json.AC_out_voltage | float"						"V"		"power-plug"
registerTopicToHA "AC out frequency"			"value_json.AC_out_frequency | float"					"Hz"	"current-ac"
registerTopicToHA "PV in voltage"				"value_json.PV_in_voltage | float"						"V"		"solar-panel-large"
registerTopicToHA "PV in current"				"value_json.PV_in_current | float"						"A"		"solar-panel-large"
registerTopicToHA "PV in watts"					"value_json.PV_in_watts | float"						"W"		"solar-panel-large"
registerTopicToHA "PV in watthour"				"value_json.PV_in_watthour | float"						"Wh"	"solar-panel-large"
registerTopicToHA "SCC voltage"					"value_json.SCC_voltage | float"						"V"		"current-dc"
registerTopicToHA "Load pct"					"value_json.Load_pct | float"							"%"		"brightness-percent"
registerTopicToHA "Load watt"					"value_json.Load_watt | float"							"W"		"chart-bell-curve"
registerTopicToHA "Load watthour"				"value_json.Load_watthour | float"						"Wh"	"chart-bell-curve"
registerTopicToHA "Load VA"						"value_json.Load_va | float"							"VA"	"chart-bell-curve"
registerTopicToHA "Bus voltage"					"value_json.Bus_voltage | float"						"V"		"details"
registerTopicToHA "Heatsink temperature"		"(value_json.Heatsink_temperature | float) / 10" 		"°C"	"details"
registerTopicToHA "Battery capacity"			"value_json.Battery_capacity | float"					"%"		"battery-outline"
registerTopicToHA "Battery voltage"				"value_json.Battery_voltage | float"					"V"		"battery-outline"
registerTopicToHA "Battery charge current"		"value_json.Battery_charge_current | float"				"A"		"current-dc"
registerTopicToHA "Battery discharge current"	"value_json.Battery_discharge_current | float"			"A"		"current-dc"
registerTopicToHA "Load status on"				"value_json.Load_status_on == 1"						""		"power"
registerTopicToHA "SCC charge on"				"value_json.SCC_charge_on == 1"							""		"power"
registerTopicToHA "AC charge on"				"value_json.AC_charge_on == 1"							""		"power"
registerTopicToHA "Battery recharge voltage"	"value_json.Battery_recharge_voltage | float"			"V"		"current-dc"
registerTopicToHA "Battery under voltage"		"value_json.Battery_under_voltage | float"				"V"		"current-dc"
registerTopicToHA "Battery bulk voltage"		"value_json.Battery_bulk_voltage | float"				"V"		"current-dc"
registerTopicToHA "Battery float voltage"		"value_json.Battery_float_voltage | float"				"V"		"current-dc"
registerTopicToHA "Max grid charge current"		"value_json.Max_grid_charge_current | float"			"A"		"current-ac"
registerTopicToHA "Max charge current"			"value_json.Max_charge_current | float"					"A"		"current-ac"
registerTopicToHA "Out source priority"			"value_json.Out_source_priority | int"					""		"grid"
registerTopicToHA "Charger source priority"		"value_json.Charger_source_priority | int"				""		"solar-power"
registerTopicToHA "Battery redischarge voltage"	"value_json.Battery_redischarge_voltage | float"		"V"		"battery-negative"
registerTopicToHA "Warnings"					"value_json.Warnings"									""		"alert"

# Add in a separate topic so we can send raw commands from assistant back to the inverter via MQTT (such as changing power modes etc)...
registerInverterRawCMDToHA


mosquitto_pub -h $MQTT_SERVER -p $MQTT_PORT -u "$MQTT_USERNAME" -P "$MQTT_PASSWORD" -t "$MQTT_TOPIC/$INV_DEVICENAME_CLEANED/status" -r -m "Online"