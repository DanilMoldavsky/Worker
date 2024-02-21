from telebot import types
from gpt.gpt import Gpt
from db.sqlite import SQLite
import telebot
import requests
import time
#! markdown info https://paulradzkov.com/2014/markdown_cheatsheet/ , https://codepen.io/paulradzkov/pen/ZGoLgr , https://core.telegram.org/bots/api#markdownv2-style

# https://habr.com/ru/articles/675404/ - неплохой бот на telebot

bot = telebot.TeleBot('6004800515:AAHaoQJ2kgfofcjrRdQJd1IMMJP8GQKXM_M')
db = SQLite("db\\dialogs_context.db")
gpt = Gpt()
MEMORY = True

# table = db.table
# ID_PERS = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    full = types.KeyboardButton('Полный скрипт')
    markup.add(full)#, btn2
    bot.send_message(message.chat.id, '''👋 Привет!
💎 С помощью этого бота ты сможешь общаться с чатом *Gpt4*! Бот сохраняет историю диалогов и gpt может вести диалог 🗣
📲 Чтобы начать просто пришли любой текст не длиннее `4700` символов ✏
                     ''', parse_mode="Markdown")


@bot.message_handler(commands=['myid'])
def send_id(message):
    # bot.send_message('@pon4ik_channel', f'{message.channel.id}') # https://t.me/pon4ik_channel
    bot.send_message(message.from_user.id, f'{message.from_user.id}')


@bot.message_handler(commands=['memory'])
def memory_command(message):
    global MEMORY
    MEMORY = not MEMORY
    bot.reply_to(message, "Memory enabled" if MEMORY == True else "Memory disabled")



@bot.message_handler(content_types=['text'])
def get_user_text(message):
    try:
        global TABLE, MEMORY, USERNAME, db, gpt
        USERNAME = message.from_user.username
        ID_USER = message.from_user.id
        system_prompt = ''
        
        TABLE = USERNAME
        db.create_table_if_not(TABLE, MEMORY)
        
        # global table
        # global ID_PERS
        # global ID_MESSAGE_EDIT
        
        # db=SQLite("db\\dialogs.db")
        gpt.prompts = message.text
        
        db.take_all(TABLE)
        
        system_prompt = system_prompt + "To answer the next question these data may be relevant: "
        
        # for el in db.rows:
        #     if len(system_prompt) >=4500:
        #         system_prompt = system_prompt[:4000]
        #         break
                
        #     system_prompt += el[0] + ' '
        
        # messages = [{"role": "user", "content": {gpt.prompts}}]
        # context = db.take_context()
        # messages.extend(context)
        
        # system_prompt = 'To format text, use markdownv2 for telegram. This is the previous history of your dialogue with this person, take it into consideration: ' 
        response = gpt.talk_valid_markdown(prompts=gpt.prompts)
        
        bot.send_message(message.from_user.id, response, parse_mode="Markdown")
        
        
        # if MEMORY == True:
        #     try:
        #         db.insert(TABLE, gpt.prompts, 'user')
        #         db.insert(TABLE, response, 'assistant')
        #     except Exception as e:
        #         print(e)
        #         bot.send_message(722895694, e)
                
        #     db.take_all(TABLE)
            
            
        #     #     print(type(el))
        #     #     bot.send_message(722895694, el)
        #     #     time.sleep(2)
                
                
            
        #     print(db.rows)
        #     # print(type(db.rows))
        
        
            
    except Exception as e:
        print(e)
        with open('log_tg.txt', 'a', encoding="utf-8") as file:
            file.write(f'\n{str(e)}')
        bot.send_message(message.from_user.id,  '''Простите, сейчас мой создатель меня дорабатывает, попробуйте позже 
        Если проблема *долго* не решается напишите нашему создателю *@Sad_Manners*
                         ''', parse_mode="Markdown")
        # db.show_all()
        
        # if len(db.rows) > 0 or res[0] != []:
        #     system_prompt = system_prompt + "To answer the next question these data may be relevant: "
        #     for i in res:
        #         if (len(i) > 0):
        #             system_prompt = system_prompt + i[0]


if __name__ == '__main__':
    bot.polling(none_stop=True)
