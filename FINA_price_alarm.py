import pandas as pd
import time
import telegram
from datetime import datetime
from pytz import timezone
import requests

TOKEN = "" #bot token 

def send_telegram_message(msg, token=TOKEN):
    try:
        chat_id =  #add chat id to send messages
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chat_id,text=msg)
    except ConnectionError as e:
        print("Error in connection, trying to send message again.")
        time.sleep(30)
        send_telegram_message(message)
        return
    return

def price_request_fina():
    data = requests.get('https://api.pancakeswap.info/api/v2/tokens/0x426c72701833fddbdfc06c944737c6031645c708').json()
    df = pd.DataFrame(data)
    return float(df['data']['price'])

price_min_max = [0.7,1.3]
counts_min_max = 0
message = "Checking FINA variations lower than %.2f USDT or higher %.2f USDT"%(price_min_max[0],price_min_max[1])
send_telegram_message(message)
while True:
    current_time = datetime.now(timezone('Europe/Berlin')).strftime("%H:%M:%S")  #time
    time_to_sleep = 300
    price = price_request_fina()
    if(price > price_min_max[1]):
        message = "The price of FINA increased until %.3f"%price
        if(counts_min_max > 5):
            message = "Increasing higher price check from %.2f USDT to %.2f USDT"%(price_min_max[1],1.01*price)
            price_min_max[1]=1.01*price
            counts_min_max = 0
            send_telegram_message(message)
    if(price < price_min_max[0]):
        message = "The price of FINA decreased until %.3f"%price
        if(counts_min_max > 5):
            message = "Reducing lower price check from %.2f USDT to %.2f USDT"%(price_min_max[0],0.99*price)
            price_min_max[0]=0.99*price
            counts_min_max = 0
            send_telegram_message(message)
            
    if(price > price_min_max[1] or price < price_min_max[0]):
       send_telegram_message(message)
       time_to_sleep = 60
       counts_min_max += 1
    print("Sleeping %i sec with a FINA price of %.3f USDT"%(time_to_sleep,price),current_time)
    time.sleep(time_to_sleep)
