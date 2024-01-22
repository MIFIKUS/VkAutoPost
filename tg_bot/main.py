import json

import telebot

def _get_token():
    with open('service_files\\tg.json') as tg_cnf:
        return json.load(tg_cnf).get('API_KEY')
def _get_admin_id():
    with open('service_files\\tg.json') as tg_cnf:
        return json.load(tg_cnf).get('ADMIN_ID')

_token = _get_token()
_admin_id = _get_admin_id()
bot = telebot.TeleBot(_token)

def _create_post(self, msg):
    with open('tg_bot\\post\\post_text.txt', 'w+', encoding='utf-8') as post_text:
        post_text.write(msg.text)
    fileID = msg.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("tg_bot\\post\\post_photo.jpg", 'wb') as post_photo:
        post_photo.write(downloaded_file)

@bot.message_handler()
def make_post(message):
    if message.text == '123':
        _create_post(message)

def _send_msg(self, text):
    self.bot.send_message(self._admin_id, text)





