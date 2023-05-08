#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import subprocess
import json
import time
import os
import traceback
from threading import Lock

config_json = json.loads(open("/data/options.json").read())
inverter_devicename_cleaned = os.getenv('INV_DEVICENAME_CLEANED')

print(f"Config: {config_json}")

flag_connected = 0

print("init")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    global flag_connected
    flag_connected = 1

    try:
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/cmd")

        print("connected to mqtt")
        client.publish(f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/status", "online", 1, retain=True)

        print("publishing device...")
        public_device()

        print("publishing topics...")
        publish_ha_topic()

        print("Updating inverter state...")
        publish_inverter_state()
    except Exception as e:
        print("Unexpected error: " + str(e))
        pass


def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0
    print("disconnected from mqtt")


# The callback for when a `publish` message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    text = msg.payload.decode("utf-8")
    json_result = run_mpp_solar(text)
    if json_result:
        client.publish(f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/result", json_result, 2, retain=False)

    json_settings = run_mpp_solar("QPIRI")
    if json_settings:
        client.publish(f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/settings", json_settings, 2, retain=False)


def publish_ha_topic():
    publish_ha_sensor("settings", "conf_ac_input_voltage", "value_json.ac_input_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("settings", "conf_ac_input_current", "value_json.ac_input_current | float", "A", "details", "sensor")
    publish_ha_sensor("settings", "conf_ac_output_voltage", "value_json.ac_output_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("settings", "conf_ac_output_frequency", "value_json.ac_output_frequency | float", "Hz", "details", "sensor")
    publish_ha_sensor("settings", "conf_ac_output_current", "value_json.ac_output_current | float", "A", "details", "sensor")
    publish_ha_sensor("settings", "conf_ac_output_apparent_power", "value_json.ac_output_apparent_power | float", "VA", "details", "sensor")
    publish_ha_sensor("settings", "conf_ac_output_active_power", "value_json.ac_output_active_power | float", "W", "details", "sensor")
    publish_ha_sensor("settings", "conf_battery_voltage", "value_json.battery_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("settings", "battery_recharge_voltage", "value_json.battery_recharge_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("settings", "battery_under_voltage", "value_json.battery_bulk_charge_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("settings", "battery_bulk_charge_voltage", "value_json.ac_output_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("settings", "battery_float_charge_voltage", "value_json.battery_float_charge_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("settings", "battery_type", "value_json.battery_type", "", "details", "sensor")
    publish_ha_sensor("settings", "max_ac_charging_current", "value_json.max_ac_charging_current | float", "A", "details", "sensor")
    publish_ha_sensor("settings", "max_charging_current", "value_json.max_charging_current | float", "A", "details", "sensor")
    publish_ha_sensor("settings", "input_voltage_range", "value_json.input_voltage_range", "", "details", "sensor")
    publish_ha_sensor("settings", "output_source_priority", "value_json.output_source_priority", "", "details", "sensor")
    publish_ha_sensor("settings", "charger_source_priority", "value_json.charger_source_priority", "", "details", "sensor")
    publish_ha_sensor("settings", "max_parallel_units", "value_json.max_parallel_units | int", "", "details", "sensor")
    publish_ha_sensor("settings", "machine_type", "value_json.machine_type", "", "details", "sensor")
    publish_ha_sensor("settings", "topology", "value_json.topology", "", "details", "sensor")
    publish_ha_sensor("settings", "output_mode", "value_json.output_mode", "", "details", "sensor")
    publish_ha_sensor("settings", "battery_redischarge_voltage", "value_json.battery_redischarge_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("settings", "pv_ok_condition", "value_json.pv_ok_condition", "", "details", "sensor")
    publish_ha_sensor("settings", "pv_power_balance", "value_json.pv_power_balance", "", "details", "sensor")

    publish_ha_sensor("state", "ac_input_voltage", "value_json.ac_input_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("state", "ac_input_frequency", "value_json.ac_input_frequency | float", "Hz", "details", "sensor")
    publish_ha_sensor("state", "ac_output_voltage", "value_json.ac_output_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("state", "ac_output_frequency", "value_json.ac_output_frequency | float", "Hz", "details", "sensor")
    publish_ha_sensor("state", "ac_output_apparent_power", "value_json.ac_output_apparent_power | float", "VA", "details", "sensor")
    publish_ha_sensor("state", "ac_output_active_power", "value_json.ac_output_active_power | float", "W", "details", "sensor")
    publish_ha_sensor("state", "ac_output_load", "value_json.ac_output_load | float", "%", "details", "sensor")
    publish_ha_sensor("state", "bus_voltage", "value_json.bus_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("state", "battery_voltage", "value_json.battery_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("state", "battery_charging_current", "value_json.battery_charging_current | float", "A", "details", "sensor")
    publish_ha_sensor("state", "battery_capacity", "value_json.battery_capacity | float", "%", "details", "sensor")
    publish_ha_sensor("state", "inverter_heat_sink_temperature", "value_json.inverter_heat_sink_temperature | float", "°C", "details", "sensor")
    publish_ha_sensor("state", "pv_input_current_for_battery", "value_json.pv_input_current_for_battery | float", "A", "details", "sensor")
    publish_ha_sensor("state", "pv_input_voltage", "value_json.pv_input_voltage | float", "V", "details", "sensor")
    publish_ha_sensor("state", "battery_voltage_from_scc", "value_json.battery_voltage_from_scc | float", "V", "details", "sensor")
    publish_ha_sensor("state", "battery_discharge_current", "value_json.battery_discharge_current | float", "A", "details", "sensor")
    publish_ha_sensor("state", "is_sbu_priority_version_added", "value_json.is_sbu_priority_version_added", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_configuration_changed", "value_json.is_configuration_changed", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_scc_firmware_updated", "value_json.is_scc_firmware_updated", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_load_on", "value_json.is_load_on", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_battery_voltage_to_steady_while_charging", "value_json.is_battery_voltage_to_steady_while_charging", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_charging_on", "value_json.is_charging_on", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_scc_charging_on", "value_json.is_scc_charging_on", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_ac_charging_on", "value_json.is_ac_charging_on", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "rsv1", "value_json.rsv1", "", "details", "sensor")
    publish_ha_sensor("state", "rsv2", "value_json.rsv2", "", "details", "sensor")
    publish_ha_sensor("state", "pv_input_power", "value_json.pv_input_power | float", "W", "details", "sensor")
    publish_ha_sensor("state", "is_charging_to_float", "value_json.is_charging_to_float", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_switched_on", "value_json.is_switched_on", "", "details", "binary_sensor", 1, 0)
    publish_ha_sensor("state", "is_reserved", "value_json.is_reserved", "", "details", "binary_sensor", 1, 0)

    publish_ha_sensor("mode", "device_mode", "value_json.device_mode", "", "details", "sensor")


def publish_ha_sensor(topic, cleaned_up_name, value_template, unit_of_measurement, icon, sensor_type, payload_on=None, payload_off=None):
    global flag_connected

    if not flag_connected:
        return

    json_data = {
        "name": f"{config_json['InverterName']} {cleaned_up_name}",
        "state_topic": f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/{topic}",
        "value_template": "{{" + value_template + "}}",
        "icon": f"mdi:{icon}",
        "availability": {
            "topic": f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/status",
            "payload_available": "online",
            "payload_not_available": "offline"
        }
    }

    if unit_of_measurement:
        json_data["unit_of_measurement"] = unit_of_measurement

    if payload_on:
        json_data["payload_on"] = payload_on
    if payload_off:
        json_data["payload_off"] = payload_off

    json_data["unique_id"] = f"{inverter_devicename_cleaned}_{cleaned_up_name}"
    json_data["device"] = {
        "name": config_json['InverterName'],
        "identifiers": inverter_devicename_cleaned,
        "manufacturer": config_json['InverterManufacturer']
    }

    mqtt_client.publish(f"{config_json['haTopic']}/{sensor_type}/{inverter_devicename_cleaned}/{cleaned_up_name}/config", json.dumps(json_data), 1, retain=True)


def public_device():
    device_data = {
        "name": config_json['InverterName'],
        "state_topic": f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/cmd",
        "device": {
            "name": config_json['InverterName'],
            "identifiers": inverter_devicename_cleaned,
            "manufacturer": config_json['InverterManufacturer']
        }
    }
    mqtt_client.publish(f"{config_json['haTopic']}/{inverter_devicename_cleaned}/config", json.dumps(device_data), 1, retain=True)


lock = Lock()


def run_mpp_solar(cmd, can_skip=False):
    if lock.locked() and can_skip:
        print(f"skipping {cmd}, locked")
        return

    lock.acquire()

    try:
        # command = f'mpp-solar -p {INV_PORT} -c {cmd} -o json_mqtt,json --mqttbroker {MQTT_SERVER} --mqttport {MQTT_PORT} --mqttuser  "{MQTT_USERNAME}" --mqttpass "{MQTT_PASSWORD}" --mqtttopic "{MQTT_TOPIC}/{INV_DEVICENAME_CLEANED}/{topic}"'
        command = f'mpp-solar -p {config_json["InverterPort"]} -c {cmd} -o json'
        print(f"running command {command}")

        result = subprocess.run(command, shell=True, capture_output=True, check=False)

        if result.stderr:
            print(f"Command {result.args} Error {result.returncode} {result.stderr}")
        if result.stdout:
            print(f"Command Result: {result.stdout.decode('utf-8')}")

        return result.stdout.decode('utf-8')
    except Exception:
        print(traceback.format_exc())
        return None
    finally:
        lock.release()


def publish_inverter_state():
    if flag_connected == 1:
        time.sleep(5)
        json_settings = run_mpp_solar("QPIRI", True)
        if json_settings:
            mqtt_client.publish(f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/settings", json_settings, 2, retain=False)
        time.sleep(5)
        json_state = run_mpp_solar("QPIGS", True)
        if json_state:
            mqtt_client.publish(f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/state", json_state, 2, retain=False)
        time.sleep(5)
        json_mode = run_mpp_solar("QMOD", True)
        if json_mode:
            mqtt_client.publish(f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/mode", json_mode, 2, retain=False)


def start_loop():
    while True:
        publish_inverter_state()
        time.sleep(5)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_message = on_message

mqtt_client.username_pw_set(config_json['MqttUsername'], config_json['MqttPassword'])
mqtt_client.will_set(f"{config_json['MqttTopic']}/{inverter_devicename_cleaned}/status", "offline", 1, retain=True)

print("connecting to mqtt...")
mqtt_client.connect_async(config_json['MqttHost'], 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a manual interface.
# mqtt_client.loop_forever()

mqtt_client.loop_start()

print("Starting loop...")
start_loop()

print("The End...")
mqtt_client.loop_stop()
