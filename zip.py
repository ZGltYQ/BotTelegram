import telebot
import os
import time
from zipfile import ZipFile
bot = telebot.TeleBot('996619411:AAHfOfTx2XTPwJAZni0LM4UIpU6Vn9EbEhg')
users = [617618565]
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('/zip', '/install',"/download")
bot.send_message(users[0],"Cистема включена")
@bot.message_handler(func=lambda message: message.chat.id not in users)
def some(message):
    bot.send_message(message.chat.id, 'Я тебя не знаю и говорить с тобой я не буду.')
@bot.message_handler(content_types=['text'])
@bot.message_handler(content_types=['text'])
def send_text(message):
	if message.text == "Zip" or message.text == 'zip':
		bot.register_next_step_handler(message, get_zip)
def get_zip(message):
	file_paths = [] 
	for root, directories, files in os.walk(message.text): 
	    for filename in files: 
	        filepath = os.path.join(root, filename) 
	        file_paths.append(filepath)
	with ZipFile('backup.zip','w') as zip: 
	    for file in file_paths: 
	        zip.write(file)
	f = open('backup.zip','rb')
	bot.send_document(message.chat.id, f)
	f.close()
bot.polling()