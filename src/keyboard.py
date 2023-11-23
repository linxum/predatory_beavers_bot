from telebot import types

keys_menu = types.ReplyKeyboardMarkup(True, True)
keys_menu.add("Расписание", "Состав", "Напутствие", "Оставить заявку")

keys_admin = types.ReplyKeyboardMarkup(True, True)
keys_admin.add("Получить заявки", "Изменить расписание", "Пожелания", "Изменить состав", "Отправить пост")