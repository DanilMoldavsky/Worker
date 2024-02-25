from telebot import types
from db.sqlite import SQLite
from worker import Worker
import re
import telebot
import requests
import time

bot = telebot.TeleBot('7014412419:AAFiQ0toKgiXt4zqPlGvWpR4ojwJLfjrPgQ')
# db = SQLite("db\\dialogs_context.db")
proxy_id = "71790"
worker = Worker('webdriver/chromedriver.exe', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
MEMORY = True


# table = db.table
# ID_PERS = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # full = types.KeyboardButton('Полный скрипт')
    # markup.add(full)#, btn2
    bot.send_message(message.chat.id, '''👋 Привет!
💎 С помощью этого бота ты сможешь общаться с чатом *Gpt4*! Бот сохраняет историю диалогов и gpt может вести диалог 🗣
📲 Чтобы начать просто пришли любой текст не длиннее `4700` символов ✏
                     ''', parse_mode="Markdown")


@bot.message_handler(commands=['myid'])
def send_id(message):
    bot.send_message(message.from_user.id, f'{message.from_user.id}')


@bot.message_handler(commands=['proxy'])
def send_proxy(message):
    global proxy_id
    bot.send_message(message.from_user.id, f'Актуальный айди прокси: {proxy_id}. Хотите поменять? Нажмите /changeproxy')
    
    
@bot.message_handler(commands=['changeproxy'])
def change_proxy(message):
    bot.send_message(message.from_user.id, 'Введи айди прокси:')
    
    
@bot.message_handler(commands=['setcookie'])
def set_cookie(message):
    global worker
    bot.send_message(message.from_user.id, 'Процесс сохранения куков запущен на сервере, ожидайте...\nНапоминаю о необходимости администратора при сохранении!!!')
    worker.set_cookie()
    bot.send_message(message.from_user.id, 'Куки сохранены!')
    
    
@bot.message_handler(commands=['take'])
def take_accs(message):
    bot.send_message(message.from_user.id, '''Давай соберем аккаунты
Чтобы я начал пришли мне данные в следующем формате - *НомерСтраницы Кол-воПачек Кол-воАккаунтов НомерГруппы*
Пример - *97 1 1 1*''', parse_mode="Markdown")
    
    
@bot.message_handler(commands=['check'])
def check_accs(message):
    bot.send_message(message.from_user.id, '''Чек аккаунтов
Чтобы я начал пришли мне данные в следующем формате - *LabelГруппыНачало,LabelГруппыКонец*
Пример - *01.01 100.1,02.01.30*''', parse_mode="Markdown")
    

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    try:
        global proxy_id, worker
        PATTERN_CHECK = r"\d,\d"
        USERNAME = message.from_user.username
        ID_USER = message.from_user.id
        system_prompt = ''
        
        TABLE = USERNAME
        # db.create_table_if_not(TABLE, MEMORY)
        
        if len(message.text) == 5 and message.text.isdigit():
            proxy_id = message.text
            bot.send_message(message.from_user.id, f'Новый айди прокси: {proxy_id}')
            
        if message.text.replace(' ', '').isdigit():
            bot.send_message(message.from_user.id, 'Я начал собирать аккаунты, пожалуйста подождите...')
            
            take_list = message.text.split(' ')
            worker.take_accs(url_page=take_list[0], packs_quantity=take_list[1], 
                            accs_quantity=take_list[2], group_num=take_list[3], proxy_id=proxy_id)
            
            bot.send_message(message.from_user.id, '*Аккаунты собраны!*', parse_mode="Markdown")
        if re.search(PATTERN_CHECK, message.text):
            bot.send_message(message.from_user.id, 'Я начал чекать аккаунты, пожалуйста подождите...')
            
            check_list = message.text.split(',')
            worker.check_accs(start=check_list[0], end=check_list[1])
            
            bot.send_message(message.from_user.id, '*Аккаунты чекнуты!*', parse_mode="Markdown")
            
        
    except:
        pass
            
        
#         # global table
#         # global ID_PERS
#         # global ID_MESSAGE_EDIT
        
#         # db=SQLite("db\\dialogs.db")
#         gpt.prompts = message.text
        
#         db.take_all(TABLE)
        
#         system_prompt = system_prompt + "To answer the next question these data may be relevant: "
        
#         # for el in db.rows:
#         #     if len(system_prompt) >=4500:
#         #         system_prompt = system_prompt[:4000]
#         #         break
                
#         #     system_prompt += el[0] + ' '
        
#         # messages = [{"role": "user", "content": {gpt.prompts}}]
#         # context = db.take_context()
#         # messages.extend(context)
        
#         # system_prompt = 'To format text, use markdownv2 for telegram. This is the previous history of your dialogue with this person, take it into consideration: ' 
#         response = gpt.talk_valid_markdown(prompts=gpt.prompts)
        
#         bot.send_message(message.from_user.id, response, parse_mode="Markdown")
        
        
#         # if MEMORY == True:
#         #     try:
#         #         db.insert(TABLE, gpt.prompts, 'user')
#         #         db.insert(TABLE, response, 'assistant')
#         #     except Exception as e:
#         #         print(e)
#         #         bot.send_message(722895694, e)
                
#         #     db.take_all(TABLE)
            
            
#         #     #     print(type(el))
#         #     #     bot.send_message(722895694, el)
#         #     #     time.sleep(2)
                
                
            
#         #     print(db.rows)
#         #     # print(type(db.rows))
        
        
            
    # except Exception as e:
    #     print(e)
    #     with open('log_tg.txt', 'a', encoding="utf-8") as file:
    #         file.write(f'\n{str(e)}')
    #     bot.send_message(message.from_user.id,  '''Простите, сейчас мой создатель меня дорабатывает, попробуйте позже 
    #     Если проблема *долго* не решается напишите нашему создателю *@Sad_Manners*
    #                      ''', parse_mode="Markdown")


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print('При работе бота возникла ошибка')
            with open('log_tg.txt', 'a', encoding="utf-8") as file:
                file.write(f'\n{str(e)}')
            time.sleep(25)