import os
import requests
import telebot
from opcua import Client


url = "opc.tcp://212.205.81.18:4840/OPCUA/NORDEX-CIF-OPC-UA"
bot_token = "7046112254:AAHQS_1G4_VXObljR9-kbL_53WIbE54uzXM"

node_voltage = "ns=2;s=01CWE50208_analog_ANA000"
node_power = "ns=2;s=01CWE50208_analog_ANA006"

bot = telebot.TeleBot(bot_token)

def opc(nodeid):
    try:
        client = Client(url)
        client.connect()

        node = client.get_node(nodeid)
        value = node.get_value()

        client.disconnect()
        return value
    except Exception as err:
        return err

@bot.message_handler(commands=['v', 'voltage'])
def voltage(message):
    value = f'{opc(node_voltage):.2f} kV'
    bot.reply_to(message, value)

@bot.message_handler(commands=['p', 'power'])
def power(message):
    value = f'{opc(node_power):.2f} MW'
    bot.reply_to(message, value)

bot.infinity_polling()
