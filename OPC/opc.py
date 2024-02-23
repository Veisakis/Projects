import os
import requests
import telebot
from opcua import Client


url = "opc.tcp://212.205.81.18:4840/OPCUA/NORDEX-CIF-OPC-UA"
bot_token = "7046112254:AAHQS_1G4_VXObljR9-kbL_53WIbE54uzXM"

node_voltage = "ns=2;s=01CWE50208_analog_ANA000"
node_power = "ns=2;s=01CWE50208_analog_ANA006"
node_system = "ns=2;s=01CWE50208_analog_ANA070"
node_com = "ns=2;s=01CWE50208_analog_ANA072"
node_ws = "ns=2;s=01CWE50208_analog_ANA047"

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

@bot.message_handler(commands=['start', 'help'])
def voltage(message):
    value = "Commands\n/v - Voltage at TM\n/p - Power at TM\n/a - Availability\n/w - Wind Speed"
    bot.reply_to(message, value)

@bot.message_handler(commands=['v', 'voltage'])
def voltage(message):
    value = f'{opc(node_voltage):.2f} kV'
    bot.reply_to(message, value)

@bot.message_handler(commands=['p', 'power'])
def power(message):
    value = f'{opc(node_power):.2f} MW'
    bot.reply_to(message, value)

@bot.message_handler(commands=['a', 'availability'])
def availability(message):
    value = f'System: {opc(node_system)}/9\nCommunication: {opc(node_com)}/9'
    bot.reply_to(message, value)

@bot.message_handler(commands=['w', 'wind'])
def availability(message):
    value = f'{opc(node_ws):.2f} m/s'
    bot.reply_to(message, value)

bot.infinity_polling()
