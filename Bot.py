import telebot
import os
from sound import Sound
import pyautogui
import time
import webbrowser
from ctypes import *
from telebot import types
bot = telebot.TeleBot('1123247036:AAESQRciv8wpByNPqENWDIgjgIYbCGq-BUU')
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('/cmd', '/volume',"/find","/media")
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Mute', 'Max')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('<<','||', '>>')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('Start','Stop')
keyboard4 = types.InlineKeyboardMarkup()
callback_button1 = types.InlineKeyboardButton(text="<<", callback_data="left")
callback_button2 = types.InlineKeyboardButton(text=">>", callback_data="right")
callback_button3 = types.InlineKeyboardButton(text="||", callback_data="stop")
keyboard4.add(callback_button1,callback_button3,callback_button2)
keyboard5 = types.InlineKeyboardMarkup()
callback_button = types.InlineKeyboardButton(text="shutdown", callback_data="shutdown")
keyboard5.add(callback_button)
users = [617618565]
bot.send_message(users[0],"Cистема включена")
@bot.message_handler(commands=['menu'])
def start_message(message):
	bot.send_message(message.chat.id,'Чем могу помочь ?',reply_markup=keyboard)
@bot.message_handler(func=lambda message: message.chat.id not in users)
def some(message):
    bot.send_message(message.chat.id, 'Я тебя не знаю и говорить с тобой я не буду.')
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '/cmd':
    	bot.send_message(message.chat.id, 'Для выключения нажми',reply_markup=keyboard5)
    	bot.send_message(message.chat.id, '>>')
    	bot.register_next_step_handler(message, get_cmd)
    elif message.text.lower() == "/volume":
    	vol = Sound.current_volume()
    	bot.send_message(message.chat.id, "Громкость: %s" % (vol))
    	bot.send_message(message.chat.id, 'Какую громкость хочешь?:',reply_markup=keyboard1)
    	bot.register_next_step_handler(message, get_volume)
    elif message.text.lower() == "/find":
    	bot.send_message(message.chat.id, "Что ищем?")
    	bot.register_next_step_handler(message, get_find)
    elif message.text.lower() == "/media":
    	bot.send_message(message.chat.id, 'Если видео открыто не на полный экран то я бессилен',reply_markup=keyboard4)
    else:
    	bot.send_message(message.chat.id, 'Если не знаешь что делать напиши /menu')
def get_cmd(message):
	try:
		command = message.text.split()
		for i in command:
			if i == "dir":
				os.system("{} > output.txt".format(str(message.text)))
				uis_text = open('output.txt', 'rb')
				bot.send_document(message.chat.id, uis_text)
				uis_text.close()
				os.system("del output.txt")
			elif i == "tasklist":
				os.system("{} > output.txt".format(str(message.text)))
				uis_text = open('output.txt', 'rb')
				bot.send_document(message.chat.id, uis_text)
				uis_text.close()
				os.system("del output.txt")
			elif i == "Download" or i == "download":
				try:
					f = open(command[1], 'rb')
					bot.send_document(message.chat.id, f)
					f.close()
				except:
					bot.send_message(message.chat.id, 'Такого файла нет')
			elif i == "Install" or i == "install":
				bot.register_next_step_handler(message,get_install)
			else:
				os.system("{}".format(str(message.text)))
	except ValueError:
		bot.send_message(message.chat.id, 'Ошибка')
def get_volume(message):
	if message.text == "Mute":
		Sound.mute()
	elif message.text == "Max":
		Sound.volume_max()
	else:
		try:
			Sound.volume_set(int(message.text))
		except ValueError:
			bot.send_message(message.chat.id, 'Нужно ввести число!')
def get_find(message):
    	webbrowser.open_new_tab('https://www.google.com/search?q={}'.format(message.text))
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == "stop":
				pyautogui.press('space')
			elif call.data == "left":
				pyautogui.press('left')
			elif call.data == "right":
				pyautogui.press('right')
			elif call.data == "shutdown":
				os.system("shutdown /s /t 0")
	except:
		bot.send_message(message.chat.id, "Error!")
def get_install(message):
    save_dir = os.getcwd()
    s = "Сахраняю в {}".format(save_dir)
    bot.send_message(message.chat.id, str(s))
    file_id = message.document.file_name
    file_id_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_id_info.file_path)
    src = file_id
    with open(save_dir + "/" + src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, "Файл добавлен:\nИмя файла - {}\nРасположение - {}".format(str(file_id), str(save_dir)))
bot.polling()