import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6911831983:AAFi2c8qwuOGt1OCZGDE1NM_u6VIjY-7oVw", state_storage=state_storage,
                      parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Тест на реал сигму"
text_button_1 = "Канал-легенда с блокбастерами"
text_button_2 = "Канал-легенда с майном"
text_button_3 = "Канал-легенда 1 с блокбастерами"
menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(text_poll,
                                 ))
menu_keyboard.add(telebot.types.KeyboardButton(
    text_button_1, )
)
menu_keyboard.add(telebot.types.KeyboardButton(
    text_button_2, ),
    telebot.types.KeyboardButton(text_button_3,
                                 ))


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(message.chat.id,
                     'Привет! Что будем делать?', reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Как *тебя* зовут?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! Мамикс или А4?')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id,
                 'Если а4 - держи [a4] (https://www.youtube.com/@A4a4a4a4), если мамикс - ты реал сигма держи [мамикса] (https://www.youtube.com/@ItsMamix)',
                 reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message): bot.send_message(message.chat.id, "Держи канал с блокбастерами ("
                                                             "https://www.youtube.com/@Strashikka_007) , "
                                                             "reply_markup=menu_keyboard)")

@ bot.message_handler(func=lambda message: text_button_2 == message.text)


def help_command(message):
    bot.send_message(message.chat.id, "Держи канал-легенду с майном(https://www.youtube.com/@goldvay3244) , "
                                      "reply_markup=menu_keyboard)")
@ bot.message_handler(func=lambda message: text_button_3 == message.text)


def help_command(message): bot.send_message(message.chat.id,
                                            "Еще один канал-легенда(https://www.youtube.com/@svinkaa) c блокбастерами",
                                            reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.infinity_polling()