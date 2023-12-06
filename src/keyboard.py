from telebot import types

keys_menu = types.ReplyKeyboardMarkup(True, True)
keys_menu.row('Расписание матчей🗓')
keys_menu.row('Наши составы👥')
keys_menu.row('Сообщение игрокам💌')
keys_menu.row('Вступить в ХБ🦫')
keys_menu.row('О нас📌')

keys_admin = types.ReplyKeyboardMarkup(True, True)
keys_admin.add("Получить заявки", "Изменить расписание", "Пожелания", "Изменить состав", "Отправить пост")

key_cancel = types.InlineKeyboardMarkup()
key_cancel.add(types.InlineKeyboardButton(text="Назад", callback_data="cancel"))
