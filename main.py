import telebot
from telebot import types
import json

# Создаем объект бота
bot = telebot.TeleBot("1993451876:AAGnKf1H7Nz2C22JqeAAJ6cxQEnzq26tDKo")

# Словарь для хранения групп и их учеников с оценками
groups = {}
current_group = ''
current_student = ''
filename='groups.json'

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Список групп')
    itembtn2 = types.KeyboardButton('Добавить группу')
    itembtn3 = types.KeyboardButton('Считать список')
    itembtn4 = types.KeyboardButton('Сохранить список')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Обработчик команды "Список групп"
@bot.message_handler(func=lambda message: message.text == "Список групп")
def list_groups(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for group in groups:
        itembtn = types.KeyboardButton(group)
        markup.add(itembtn)
    itembtn = types.KeyboardButton('Назад')
    markup.add(itembtn)
    bot.send_message(message.chat.id, "Выберите группу:", reply_markup=markup)

# Обработчик команды "Добавить группу"
@bot.message_handler(func=lambda message: message.text == "Добавить группу")
def add_group(message):
    bot.send_message(message.chat.id, "Введите название группы:")
    bot.register_next_step_handler(message, add_group_handler)

# Обработчик команды "Считать список"
@bot.message_handler(func=lambda message: message.text == "Считать список")
def read_groups(message):
    global groups
    try:
        with open(filename, 'r') as file:
            groups = json.load(file)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл с группами отсутствует")
    #start(message)
    list_groups(message)




# Обработчик команды "Сохранить список"
@bot.message_handler(func=lambda message: message.text == "Сохранить список")
def write_groups(message):
    with open(filename, 'w') as file:
        json.dump(groups, file, indent=4)
    start(message)


def add_group_handler(message):
    group_name = message.text
    if group_name not in groups:
        groups[group_name] = {}
        bot.send_message(message.chat.id, f"Группа '{group_name}' успешно добавлена!")
    else:
        bot.send_message(message.chat.id, "Такая группа уже существует!")
    start(message)

# Обработчик выбора группы
@bot.message_handler(func=lambda message: message.text in groups)
def group_menu(message):
    group_name = message.text
    if message.text in groups:
        global current_group
        current_group = group_name

    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Список учеников')
    itembtn2 = types.KeyboardButton('Добавить ученика')
    itembtn3 = types.KeyboardButton('Удалить ученика')
    itembtn4 = types.KeyboardButton('Назад')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, f"Группа '{current_group}':", reply_markup=markup)

# Обработчик команды "Список учеников"
@bot.message_handler(func=lambda message: message.text == "Список учеников")
def list_students(message):

    #group_name = get_current_group(message)
    group_name = current_group
    if group_name:
        students = groups[group_name]
        if students:
            #response = "Список учеников:\n"
            markup = types.ReplyKeyboardMarkup(row_width=2)
            for student in students:
                itembtn = types.KeyboardButton(student)
                markup.add(itembtn)
            itembtn = types.KeyboardButton('Back')
            markup.add(itembtn)
            bot.send_message(message.chat.id, "Выберите студента", reply_markup=markup)
            #for student in students:
            #    response += f"{student}\n"
            #bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "В этой группе пока нет учеников.")
    else:
        bot.send_message(message.chat.id, "Сначала выберите группу.")

# Обработчик команды "Добавить ученика"
@bot.message_handler(func=lambda message: message.text == "Добавить ученика")
def add_student(message):
    #group_name = get_current_group(message)
    group_name = current_group
    if group_name:
        bot.send_message(message.chat.id, "Введите имя ученика:")
        bot.register_next_step_handler(message, add_student_handler, group_name)
    else:
        bot.send_message(message.chat.id, "Сначала выберите группу.")

def add_student_handler(message, group_name):
    student_name = message.text
    if student_name not in groups[group_name]:
        groups[group_name][student_name] = []
        bot.send_message(message.chat.id, f"Ученик '{student_name}' успешно добавлен в группу '{group_name}'!")
    else:
        bot.send_message(message.chat.id, "Такой ученик уже существует в этой группе!")

    group_menu(message)

# Обработчик команды "Удалить ученика"
@bot.message_handler(func=lambda message: message.text == "Удалить ученика")
def remove_student(message):
    #group_name = get_current_group(message)
    group_name = current_group

    if group_name:
        students = groups[group_name]
        if students:
            markup = types.ReplyKeyboardMarkup(row_width=2)
            for student in students:
                itembtn = types.KeyboardButton(student)
                markup.add(itembtn)
            itembtn = types.KeyboardButton('Back')
            markup.add(itembtn)
            bot.send_message(message.chat.id, "Выберите ученика для удаления:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "В этой группе пока нет учеников.")
    else:
        bot.send_message(message.chat.id, "Сначала выберите группу.")

# # Обработчик выбора ученика для удаления
# @bot.message_handler(func=lambda message: message.text in get_students(message))
# def remove_student_handler(message):
#     #group_name = get_current_group(message)
#     group_name = current_group
#     student_name = message.text
#     del groups[group_name][student_name]
#     bot.send_message(message.chat.id, f"Ученик '{student_name}' успешно удален из группы '{group_name}'!")
#     group_menu(message)

# Обработчик выбора ученика для оценивания
@bot.message_handler(func=lambda message: message.text in get_students(message))
def grades_student_handler(message):
    #group_name = get_current_group(message)
    global current_student
    group_name = current_group
    student_name = message.text
    current_student=student_name
    #bot.send_message(message.chat.id, f"Выбран ученик '{student_name}' в группе '{group_name}'!")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Добавить оценку')
    itembtn2 = types.KeyboardButton('Удалить оценку')
    itembtn3 = types.KeyboardButton('Просмотреть оценки')
    itembtn4 = types.KeyboardButton('Назад')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, f"Выбран ученик '{student_name}' в группе '{group_name}'!", reply_markup=markup)
    #group_menu(message)

# Обработчик команды "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    start(message)

# Обработчик команды "Просмотреть оценки"
@bot.message_handler(func=lambda message: message.text == "Просмотреть оценки")
def show_grades(message):
    grades=groups[current_group[current_student]]
    bot.send_message(message.chat.id, grades)

# Обработчик команды "Назад" (группа учеников)
@bot.message_handler(func=lambda message: message.text == "Back")
def back(message):
    #start(message)
    group_menu(message)


# Функция для получения текущей группы
def get_current_group(message):
    for group in groups:
        if message.text in group:
            return group
    return None

# Функция для получения списка учеников группы
def get_students(message):
    #group_name = get_current_group(message)
    group_name = current_group
    if group_name:
        return list(groups[group_name].keys())
    return []

# Запускаем бота
bot.polling()
