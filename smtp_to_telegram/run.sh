#!/usr/bin/with-contenv bashio

CONFIG_PATH=/data/options.json

export ST_TELEGRAM_BOT_TOKEN="$(bashio::config 'ST_TELEGRAM_BOT_TOKEN')"
export ST_TELEGRAM_CHAT_IDS="$(bashio::config 'ST_TELEGRAM_CHAT_IDS')"

echo "Starting up!"

/smtp_to_telegram
