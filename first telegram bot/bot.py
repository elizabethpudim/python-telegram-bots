import telebot
import config
import random
import urllib

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('sticker.webp','rb')

	#keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton('🤗 Рандомное число')
	item2 = types.KeyboardButton('😏 Как дела?')
	markup.add(item1, item2)


	bot.send_sticker(message.chat.id, sti)
	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ-<b>{1.first_name}</b>, созданный повелителем.".format(message.from_user, bot.get_me()), parse_mode="html", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == '🤗 Рандомное число':
			bot.send_message(message.chat.id, str(random.randint(0,100)))
		elif message.text == '😏 Как дела?':
			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton('Хорошо', callback_data='good')
			item2 = types.InlineKeyboardButton('Не очень хорошо', callback_data='bad')
			markup.add(item1, item2)

			bot.send_message(message.chat.id, "Отлично, сам как?", reply_markup=markup)
		else:
			bot.send_message(message.chat.id, "Не знаю, что ответить")

@bot.message_handler(content_types=['photo'])
def image_handler(message):
	bot.send_message(message.chat.id, "Вы отправили картинку")
	bot.send_photo(message.chat.id, message.photo[-1].file_id)
	photo_id = message.photo[-1].file_id
	file_path = bot.get_file(photo_id).file_path
	image_url = "https://api.telegram.org/file/bot{0}/{1}".format(config.TOKEN, file_path)
	urllib.request.urlretrieve(image_url, "image.jpg")
	bot.send_message(message.chat.id, "Картинка успешно сохранена")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                reply_markup=None)
 
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
 
    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)