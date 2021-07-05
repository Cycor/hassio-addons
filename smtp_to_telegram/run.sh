#!/usr/bin/env bashio
set -e

CONFIG_PATH=/data/options.json

export ST_TELEGRAM_BOT_TOKEN="$(bashio::config 'ST_TELEGRAM_BOT_TOKEN')"
export ST_TELEGRAM_CHAT_IDS="$(bashio::config 'ST_TELEGRAM_CHAT_IDS')"

/smtp_to_telegram