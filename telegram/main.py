import telebot
from telebot import types
import pandas as pd
import psycopg2
from psycopg2 import Error

bot=telebot.TeleBot('6289568645:AAE6Pqf43NZ29H8lKczsYyoRjQdiZX0vG4g')
name = '';
surname = '';
age = 0;
FI=[]
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');

def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);


def get_surname(message):
    global surname;
    surname = message.text;
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Тебя зовут '+name+' '+surname+'?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def check(message):
    global surname;
    global name;
    try:
        print('Соединение установленно')
        connection = psycopg2.connect(
            user='postgres',
            password='1002amor',
            host='localhost',
            port="5432",
            database="telegram")

        cursor = connection.cursor()
        cursor.execute("SELECT student.id from public.student WHERE (name = '{}' and surename = '{}')".format(name,surname))
        #bot.send_message('заебись');
        #bot.register_next_step_handler(message, get_surname);
    except(Exception, Error) as error:
        print(error)
        print('Ошибка при работе с PostgreSQL')
        bot.send_message(message.from_user.id, 'Студент не найден');
        bot.send_message(message.from_user.id, 'Как тебя зовут?');
        bot.register_next_step_handler(message, start);
    finally:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, "проверяем базу пентагона");
        bot.register_next_step_handler(call.message,check);
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Как тебя зовут?");
        bot.register_next_step_handler(call.message, get_name);  # следующий шаг – функция get_name

#переспрашиваем
bot.delete_webhook()
bot.polling(none_stop=True, interval=0)

