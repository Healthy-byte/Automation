import telepot
import time
from secrets import token


def msg_rcv(msg):
    '''
    Denn funktion behandler modtagelse af beskeder fra
    Telegram applikationen. Funktionen tager et argument
    "msg" hvilket er et dictionary. Dette argument bliver
    givet af telebot bibliotekets API. Denne funktion bruges
    til at fremfinde chat_id til brugeren som indsættes i 
    secrets.py filen. 
    '''
    chat_id = msg['chat']['id']
    print (chat_id)
    bot.sendMessage(chat_id,chat_id)


bot = telepot.Bot(token)
bot.message_loop(msg_rcv)
print("I am listening...")
while 1:
    time.sleep(10)