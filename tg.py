from worker import Worker
import re
import telebot
import time

bot = telebot.TeleBot('7014412419:AAFiQ0toKgiXt4zqPlGvWpR4ojwJLfjrPgQ')
proxy_id = "408715"
worker = Worker('webdriver/chromedriver.exe', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')


@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id, '''👋 *Привет*
💎 Этот бот создан, чтобы показать, что даже такую работу можно оптимизировать 🗣
📲 Бот будет работать вместо вас, в данный момент настроен на работу с фейсбуком ✏
                     ''', parse_mode="MarkdownV2")


@bot.message_handler(commands=['myid'])
def send_id(message):
    """
    Handle the 'myid' command and send the user's ID back to them.
    """
    bot.send_message(message.from_user.id, f'{message.from_user.id}')


@bot.message_handler(commands=['proxy'])
def send_proxy(message):
    """
    Handles the 'proxy' command and sends the current proxy ID to the user.
    
    Args:
        message: The message object
    """
    global proxy_id
    bot.send_message(message.from_user.id, f'Актуальный айди прокси: {proxy_id}. Хотите поменять? Нажмите /changeproxy')
    
    
@bot.message_handler(commands=['changeproxy'])
def change_proxy(message):
    """
    Handles the 'changeproxy' command by sending a message to the user to input a proxy ID.
    
    Parameters:
    - message: the message object
    """
    bot.send_message(message.from_user.id, 'Введи айди прокси:')
    
    
@bot.message_handler(commands=['setcookie'])
def set_cookie(message):
    """
    Handle the 'setcookie' command by sending a message to the user, setting a cookie using the global worker, 
    and sending another message to the user.
    """
    global worker
    bot.send_message(message.from_user.id, 'Процесс сохранения куков запущен на сервере, ожидайте...\nНапоминаю о необходимости администратора при сохранении!!!')
    worker.set_cookie()
    bot.send_message(message.from_user.id, 'Куки сохранены!')
    
    
@bot.message_handler(commands=['take'])
def take_accs(message):
    """
    A function to handle the 'take' command for the bot. It sends a message to the user requesting data in a specific format.
    """
    bot.send_message(message.from_user.id, '''Давай соберем аккаунты
Чтобы я начал пришли мне данные в следующем формате - *НомерСтраницы Кол-воПачек Кол-воАккаунтов НомерГруппы*
Пример - *97 1 1 1*''', parse_mode="Markdown")
    
    
@bot.message_handler(commands=['check'])
def check_accs(message):
    """
    A function to handle the 'check' command for the bot's message handler.
    It sends a message to the user with instructions on how to send data in a specific format. 
    """
    bot.send_message(message.from_user.id, '''Чек аккаунтов
Чтобы я начал пришли мне данные в следующем формате - *LabelГруппыНачало,LabelГруппыКонец*
Пример - *01.01 100.1,02.01.30*''', parse_mode="Markdown")


@bot.message_handler(commands=['pages'])
def create_pages(message):
    """
    A function to handle the 'pages' command and create pages based on the provided data format.
    
    Parameters:
    - message: the message object containing the command
    """
    bot.send_message(message.from_user.id, '''Создание фанпейджей
Чтобы я начал пришли мне данные в следующем формате - *pgLabelГруппыНачало,LabelГруппыКонец*
Пример - *pg01.01 100.1,02.01.30*''', parse_mode="Markdown")
    

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    """
    A function to handle text messages from the bot and perform various actions based on the text content.
    """
    global proxy_id, worker
    PATTERN_TAKE = r"\d \d$"
    PATTERN_CHECK = r"\d,\d"
    PATTERN_CREATE = r"^pg"
    
    if len(message.text) == 5 and message.text.isdigit():
        proxy_id = message.text
        bot.send_message(message.from_user.id, f'Новый айди прокси: {proxy_id}')
        
    if re.search(PATTERN_TAKE, message.text):
        bot.send_message(message.from_user.id, 'Я начал собирать аккаунты, пожалуйста подождите...')
        
        take_list = message.text.split(' ')
        worker.take_accs(url_page=take_list[0], packs_quantity=int(take_list[1]), 
                        accs_quantity=int(take_list[2]), group_num=int(take_list[3]), proxy_id=proxy_id)
        
        bot.send_message(message.from_user.id, '*Аккаунты собраны!*', parse_mode="Markdown")

    if re.search(PATTERN_CHECK, message.text) and not re.search(PATTERN_CREATE, message.text.lower()):
        bot.send_message(message.from_user.id, 'Я начал чекать аккаунты, пожалуйста подождите...')
        
        check_list = message.text.split(',')
        worker.check_accs(start=check_list[0], end=check_list[1])
        
        bot.send_message(message.from_user.id, '*Аккаунты чекнуты!*', parse_mode="Markdown")
    
    if re.search(PATTERN_CHECK, message.text) and re.search(PATTERN_CREATE, message.text.lower()):
        bot.send_message(message.from_user.id, 'Я начал создание фанпейджей, пожалуйста подождите...')
        
        page_list = message.text[2:].split(',')
        errors = worker.create_pages(start=page_list[0], end=page_list[1])
        
        bot.send_message(message.from_user.id, '*Фанпейджи созданы!*', parse_mode="Markdown")
        bot.send_message(message.from_user.id, errors, parse_mode="Markdown")


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print('При работе бота возникла ошибка')
            with open('log_tg.txt', 'a', encoding="utf-8") as file:
                file.write(f'\n{str(e)}')
            time.sleep(25)