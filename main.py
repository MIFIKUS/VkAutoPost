import time

from autoposter.auth import Login
from autoposter.poster import MakePost
from logger.logs import Logs
from tg_bot import buttons
from autoposter.get_id import get_id_by_link

import json
import telebot

log = Logs()

def _get_token():
    with open('VkAutoPost\\service_files\\tg.json') as tg_cnf:
        return json.load(tg_cnf).get('API_KEY')
def _get_admin_id():
    with open('service_files\\tg.json') as tg_cnf:
        return json.load(tg_cnf).get('ADMIN_ID')

log.log('Бот запущен')
_token = _get_token()
log.success(f'Токен тг получен {_token}')

_admin_id = _get_admin_id()
log.success(f'ID админа получено {_admin_id}')

bot = telebot.TeleBot(_token)
log.success('Тг бот инициализирован')

try:
    login = Login()
    log.success('Удалось залогиниться в вк')
except:
    log.error('Не удалось залогиниться в вк')

vk = login.get_vk()

vk_session = login.get_session()
make_post = MakePost(vk, vk_session)

def _create_post_text(msg):
    log.log("Попытка создать текст поста")
    msg.text = msg.text.replace('/create_text', '')
    with open('tg_bot\\post\\post_text.txt', 'w+', encoding='utf-8') as post_text:
        post_text.write(msg.text)
    log.success("Текст поста создан")

def _create_post_photo(msg):
    log.log("Попытка получить фото поста")
    fileID = msg.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("tg_bot\\post\\post_photo.jpg", 'wb') as post_photo:
        post_photo.write(downloaded_file)
    log.success("Удалось получить фото поста")

def _set_receivers(msg):
    log.log('Попытка заполнить список получателей')
    text = ''
    print('msg_text ', msg.text)
    for link in msg.text.split('\n'):
        log.log(f"Ссылка {link}")
        link = str(get_id_by_link(vk_session, link))
        log.log(f'ID ссылки {link}')

        if len(link) != 0:
            text += link + '\n'
            log.success('Удалось добавить ссылку')
        else:
            log.warning('Пустая строка')

    with open('tg_bot\\post\\receivers.txt', 'w+', encoding='utf-8') as receivers:
        receivers.write(text)
    log.success("ID ссылок записаны")

@bot.message_handler(commands=['start'])
def start_bot(message):
    log.log("Введена команда /start")
    bot.send_message(_admin_id, 'Выберете что хотите сделать', reply_markup=buttons.main_keyboard())

@bot.message_handler(commands=['set_receivers'])
def get_receivers(message):
    log.log("Введена команда /set_receivers")
    _set_receivers(message)

@bot.message_handler(commands=['create_text'])
def get_post_text(message):
    log.log("Введена команда /create_text")
    _create_post_text(message)
    bot.send_message(_admin_id, 'Отправьте картинку к посту')

@bot.message_handler(commands=['set_token'])
def set_vk_token(message):
    log.log("Введена команда /set_token")
    message = message.text.replace('/set_token', '')
    message = message.replace(' ', '')
    message = message.replace('\n', '')

    log.log(f'Полученный токен от вк в сообщении {message}')

    with open('service_files\\vk.json',  encoding='utf-8') as vk_cnf:
        old_cnf = json.load(vk_cnf)

    old_cnf['TOKEN'] = message

    new_cnf = old_cnf

    with open('service_files\\vk.json','w' , encoding='utf-8') as vk_cnf:
        json.dump(new_cnf, vk_cnf)

    log.success(f"Новый токен установлен {new_cnf}")

    bot.send_message(_admin_id, 'Новый токен установлен')

@bot.message_handler(commands=['set_timeout'])
def set_timeout(message):
    log.log("Введена команда /set_timeout")
    timeout = message.text.replace('/set_timeout', '')
    timeout = timeout.replace(' ', '')
    timeout = timeout.replace('\n', '')

    log.log(f"Полученный таймаут в сообщении {timeout}")

    with open('service_files\\timeout.txt', 'w', encoding='utf-8') as timeout_cnf:
        timeout_cnf.write(timeout)

    log.success("Удалось записать таймаут в файл")
    bot.send_message(_admin_id, 'Таймаут задан')

def start_auto_poster():
    log.log("Запущен автопостер")
    with open('service_files\\timeout.txt', encoding='utf=8') as timeout_cnf:
        timeout_cnf = int(timeout_cnf.read())
        log.log(f"Получен таймаут {timeout_cnf}")

    with open('tg_bot\\post\\receivers.txt', encoding='utf=8') as receivers_list:
        receivers = receivers_list.read().split('\n')
        log.success("Получен список получателей")
        for a in receivers:
            log.log(f"ID получателя{a}")

    with open('tg_bot\\post\\post_text.txt', encoding='utf=8') as post_text:
        text = post_text.read()
        log.success("Получен текст поста")

    for i in receivers:
        if len(i) == 0:
            continue
        try:
            log.log(f"Попытка отправить пост в группу с ID {i}")
            make_post.make_post(int(i), text)
            log.success(f'Удалось создать пост')
        except:
            log.error('Не удалось создать пост')

        time.sleep(timeout_cnf)

@bot.message_handler(content_types=['text'])
def make_post_text(message):
    print('make_post')
    if message.text == 'Изменить шаблон поста':
        bot.send_message(_admin_id, 'Напишите текст поста перед этим написав /create_text')
    if message.text == 'Задать список получателей':
        bot.send_message(_admin_id, 'Напишите список пользователей которым нужно отправлять пост перед этим написав /set_receivers')
    if message.text == 'Изменить аккаунт VK':
        bot.send_message(_admin_id, 'Напишите токен для входа в вк. Перед этим написав /set_token')
    if message.text == 'Задать задержку между постами':
        bot.send_message(_admin_id, 'Напишите задержку между постами(в секундах). Перед этим написав /set_timeout')
    if message.text == 'Старт':
        bot.send_message(_admin_id, 'Бот запущен. По окончанию работы вы получите сообщение')
        start_auto_poster()
        bot.send_message(_admin_id, 'Все посты отправлены'
                                    '')
@bot.message_handler(content_types=['photo'])
def make_post_photo(message):
    log.log('Получено фото')
    _create_post_photo(message)
    bot.send_message(_admin_id, 'Картинка для поста установлена')

bot.infinity_polling()

