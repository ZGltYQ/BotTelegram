import telebot
from telebot import types
bot = telebot.TeleBot('1123247036:AAESQRciv8wpByNPqENWDIgjgIYbCGq-BUU')
owner = "ZGltYQ"#[592269149]
user = []
separ = '\n'
message_id = None
@bot.message_handler(commands=['start'], func=lambda message: message.from_user.username == owner)
def start_message(message):
	global keyboard
	keyboard = types.InlineKeyboardMarkup()
	callback_button = types.InlineKeyboardButton(text="Я", callback_data="test")
	keyboard.add(callback_button)
	bot.send_message(message.chat.id, 'Кто ебал англичанку?\n Проголосовали:\n{}'.format(str(separ.join(user))), reply_markup=keyboard)
	global message_id
	if message_id is None:
		message_id = int(message.message_id + 1)
@bot.message_handler(commands=['clear'], func=lambda message: message.from_user.username == owner)
def start_message(message):
	user.clear()
	global message_id
	bot.delete_message(chat_id=message.chat.id,message_id=message_id)
	bot.send_message(message.chat.id, 'Кто ебал англичанку?\n Проголосовали:\n{}'.format(str(separ.join(user))), reply_markup=keyboard)
	message_id = int(message.message_id + 1)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == "test":
				if "@" + str(call.from_user.username) not in user:
					user.append("@" + str(call.from_user.username))
					bot.edit_message_text(chat_id=call.message.chat.id, text= "Кто ебал англичанку?\n Проголосовали:\n{}".format(str(separ.join(user))), message_id=message_id,reply_markup=keyboard)
	except:
		bot.send_message(call.message.message_id, "Error")
bot.polling()
