from telebot import types

def main_keyboard():
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    start_button = types.KeyboardButton("Старт")
    change_post_template_button = types.KeyboardButton("Изменить шаблон поста")
    change_vk_id_button = types.KeyboardButton('Изменить аккаунт VK')
    set_receivers_button = types.KeyboardButton('Задать список получателей')
    set_timeout_button = types.KeyboardButton("Задать задержку между постами")

    main_keyboard.add(start_button)
    main_keyboard.add(change_post_template_button)
    main_keyboard.add(change_vk_id_button)
    main_keyboard.add(set_receivers_button)
    main_keyboard.add(set_timeout_button)

    return main_keyboard