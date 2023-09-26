# gpu/сpu temp check for data science pet projects

import psutil
import telebot 

token = '___your___tg_bot___token___'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Напиши: gpu или cpu')

@bot.message_handler(content_types=['text'])
def send_text(message):
    action_function(message)

def action_function(message):
    if message.text.lower() == 'gpu':
        comand = !nvidia-settings -q GPUCoreTemp
        output = [str(x).strip() for x in temp if 'gpu:' in x]
        bot.send_message(message.chat.id, output)
    elif message.text.lower() == 'cpu': 
        output = str(psutil.sensors_temperatures()['coretemp'][1:])
        bot.send_message(message.chat.id, output)
    else:
        bot.send_message(message.chat.id, 'unknown command') 

bot.polling()
