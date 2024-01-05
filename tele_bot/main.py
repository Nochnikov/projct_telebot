import telebot
import messages
import quiz_data
from telebot import types
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

load_dotenv()

TOKEN = getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

current_question_index = 0
user_score = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.start_message
    )


@bot.message_handler(commands=['help'])
def help_fuc(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.help_message
    )


start_quiz_time = datetime.now().second


@bot.message_handler(commands=['start_quiz'])
def start_quiz(message):
    global current_question_index
    if current_question_index < len(quiz_data.questions):
        markup = types.InlineKeyboardMarkup()
        current_question = quiz_data.questions[current_question_index]
        for i, option in enumerate(current_question['options']):
            btn = types.InlineKeyboardButton(text=option, callback_data=str(i))
            markup.add(btn)

        bot.send_message(
            chat_id=message.chat.id,
            text=messages.question_message.format(current_question['question']),
            reply_markup=markup
        )
    else:
        end_quiz_time = datetime.now().second
        print(end_quiz_time)

        time_quiz = end_quiz_time - start_quiz_time
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.end_quiz_message.format(user_score, len(quiz_data.questions), time_quiz/60)
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global current_question_index, user_score
    current_question = quiz_data.questions[current_question_index]

    if call.data == str(current_question['correct-option']):
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=messages.correct_answer_message

        )
        user_score += 1
    else:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=messages.wrong_answer_message
        )

    current_question_index += 1
    start_quiz(call.message)


bot.polling(none_stop=True)
