import telebot
import requests

# Your bot token
BOT_TOKEN = '7280636476:AAGuYWynAoVUGcUp1FHoxQ-6WG-fV5iKI8c'
# Your IP2Location API key
API_KEY = '72E17199320C32A8DF7C10778CB90D86'

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Command handler for /ip
@bot.message_handler(commands=['ip'])
def send_ip_info(message):
    # Split the message text to get the IP argument
    msg_text = message.text.split()
    if len(msg_text) != 2:
        bot.reply_to(message, "Please provide an IP address. Usage: /ip <IP_ADDRESS>")
        return
    
    ip_address = msg_text[1]
    # Build the API URL with the IP address
    api_url = f'https://api.ip2location.io/?key={API_KEY}&ip={ip_address}'

    try:
        # Make the API request
        response = requests.get(api_url)
        data = response.json()

        # Check if the response contains an error
        if 'error' in data:
            bot.reply_to(message, f"Error: {data['error']['message']}")
            return

        # Format the response into a nice message
        location_info = (
            f"**IP Information**\n\n"
            f"**IP Address**: {data['ip']}\n"
            f"**Country**: {data['country_name']} ({data['country_code']})\n"
            f"**Region**: {data['region_name']}\n"
            f"**City**: {data['city_name']}\n"
            f"**Latitude**: {data['latitude']}\n"
            f"**Longitude**: {data['longitude']}\n"
            f"**ZIP Code**: {data['zip_code']}\n"
            f"**Time Zone**: {data['time_zone']}\n"
            f"**ASN**: {data['asn']}\n"
            f"**AS**: {data['as']}\n"
            f"**Is Proxy**: {'Yes' if data['is_proxy'] else 'No'}"
        )

        # Send the response message in Markdown format
        bot.send_message(message.chat.id, location_info, parse_mode='Markdown')

    except requests.exceptions.RequestException as e:
        # Handle any errors from the API request
        bot.reply_to(message, f"An error occurred: {e}")

# Start polling
bot.polling()