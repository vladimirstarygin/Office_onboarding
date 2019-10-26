#!/usr/bin/env python
# coding: utf-8

# In[2]:


from dialog_bot_sdk.bot import DialogBot
from dialog_api import messaging_pb2
from dialog_bot_sdk import interactive_media
from datetime import datetime
import random
import pandas as pd
import grpc


# In[3]:


#массив куда записываются входящие users
users = []
#массив куда записывается время, в которое было предыдущее Push_уведомление, будем записывать в секундах, чтобы проверять как работает
last_time = []
#создадим словарь, в котором будем записывать, какие уведомления не видел user
#При добавлении user записываем,что он не видел ни одного уведомления
user_not_seen_notification = {}
#Все уведомления будем хранить в excel csv, где будет номер уведомления, а так же само его сообщение
data = pd.read_csv("Notifications.csv",encoding='cp1251')
#Все Id уведомлений
ids = list(data["Id"].unique())
#Время, когда мы не беспокоим пользователя 1 - id, 2 - с какого, 3 - по какое время
datas = []
#Уведомления для каждого пользователя 0 - выключены, 1 - включены
notif = [] 


# In[4]:


#функция для измерения сколько прошло времени с предыдщуего push уведомления
def pass_time(last_time):
    date = datetime.now()
    #Переводим в секунды и узнаем сколько прошло
    pass_time = date.hour*60*60 + date.minute*60 + date.second - last_time
    return pass_time


# In[5]:


def RepresentInt(s):
    try: 
        number = int(s)
        if number < 0:
            return False
        else:
            return True
    except ValueError:
        return False


# In[6]:


def adding_person(id, message):
    global datas, notif
    for i in range(len(datas)):
        if id == datas[i][0]:
            if len(datas[i]) == 1:
                msg =  "Привет👋\nРады тебя видеть в нашем дружном коллективе."
                msg += "Я помогу тебе здесь освоится.\n "
                msg += "Выберите час, после которого мы вас не будем беспокоить, в интервале от 18 до 23"
                peer = bot.users.get_user_peer_by_id(id)
                bot.messaging.send_message(peer, msg)
                datas[i] += ['']
                print(len(datas[i]))
            elif len(datas[i]) == 2:
                if RepresentInt(message):
                    time = int(message)
                    if time >= 18 and time <= 23:
                        datas[i][1] = message
                        datas[i] += ['']
                        msg = "Выберите час, раньше которого мы вас не побеспокоим, в интервале от 6 до 12"
                        peer = bot.users.get_user_peer_by_id(id)
                        bot.messaging.send_message(peer, msg)
                    else:
                        msg = "Выберите час в интервале от 18 до 23"
                        peer = bot.users.get_user_peer_by_id(id)
                        bot.messaging.send_message(peer, msg)
                else:
                    msg = "Выберите час в интервале от 18 до 23"
                    peer = bot.users.get_user_peer_by_id(id)
                    bot.messaging.send_message(peer, msg)
            elif len(datas[i]) == 3:
                if datas[i][2] == '':
                    if RepresentInt(message):
                        time = int(message)
                        if time >= 6 and time <= 12:
                            datas[i][2] = message
                            msg = "С этой минуты я буду посылать тебе полезную информацию о твоей работе."
                            msg += "Заманчиво не так ли?\nТак как я на работе уже много лет, то знаю чего ты хочешь."
                            msg +=  "Скорее нажимай на кнопку и получай информацию, без которой нельзя обойтись."
                            peer = bot.users.get_user_peer_by_id(id)
                            bot.messaging.send_message(peer, msg)
                            if notif[i][1] == 1:
                                but = "Отключить уведомления"
                            else:
                                but = "Включить уведомления"
                            button_enterence = interactive_media.InteractiveMediaButton(
                                "Enterence", "Пропуск")
                            button_time = interactive_media.InteractiveMediaButton(
                                "Time", "Рабочее время")
                            button_food = interactive_media.InteractiveMediaButton(
                                "Food", "Столовая")
                            button_cansel = interactive_media.InteractiveMediaButton(
                                "Cansel", but)
                            bot.messaging.send_message(
                                peer, " ", [
                                    interactive_media.InteractiveMediaGroup([
                                        interactive_media.InteractiveMedia(
                                            1, button_enterence, style='primary'),
                                        interactive_media.InteractiveMedia(
                                            2, button_time, style='primary'),
                                        interactive_media.InteractiveMedia(
                                            3, button_food, style='primary'),
                                        interactive_media.InteractiveMedia(
                                            4, button_cansel, style='primary')])
                                ])
                        else:
                            msg = "Выберите час в интервале от 6 до 12"
                            peer = bot.users.get_user_peer_by_id(id)
                            bot.messaging.send_message(peer, msg)
                    else:
                        msg = "Выберите час в интервале от 6 до 12"
                        peer = bot.users.get_user_peer_by_id(id)
                        bot.messaging.send_message(peer, msg)
                else:
                    msg =  "Скорее нажимай на кнопку и получай информацию, без которой нельзя обойтись."
                    peer = bot.users.get_user_peer_by_id(id)
                    bot.messaging.send_message(peer, msg)
                    if notif[i][1] == 1:
                        but = "Отключить уведомления"
                    else:
                        but = "Включить уведомления"
                    button_enterence = interactive_media.InteractiveMediaButton(
                        "Enterence", "Пропуск")
                    button_time = interactive_media.InteractiveMediaButton(
                        "Time", "Рабочее время")
                    button_food = interactive_media.InteractiveMediaButton(
                        "Food", "Столовая")
                    button_cansel = interactive_media.InteractiveMediaButton(
                        "Cansel", but)
                    bot.messaging.send_message(
                        peer, " ", [
                            interactive_media.InteractiveMediaGroup([
                                interactive_media.InteractiveMedia(
                                    1, button_enterence, style='primary'),
                                interactive_media.InteractiveMedia(
                                    2, button_time, style='primary'),
                                interactive_media.InteractiveMedia(
                                    3, button_food, style='primary'),
                                interactive_media.InteractiveMedia(
                                    4, button_cansel, style='primary')])
                        ])
                


# In[7]:


def send_notification(bot, uid):
    global data
    global user_not_seen_notification
    
    
    peer = bot.users.get_user_peer_by_id(uid)
    #Если все что можно отправили, снова записываем все индексы и отправляем по новой
    if (user_not_seen_notification[uid] == []):
        user_not_seen_notification[uid] = list(data["Id"].unique())
        notific_id = random.choice(user_not_seen_notification[uid])
        bot.messaging.send_message(
        peer,
        str(data[data["Id"] == notific_id]["Notification"].values[0])
        )
    else:
        #иначе отравляем то что не отправил
        notific_id = random.choice(user_not_seen_notification[uid])
        bot.messaging.send_message(
        peer,
        str(data[data["Id"] == notific_id]["Notification"].values[0])
        )
    
    user_not_seen_notification[uid].remove(notific_id)
    


# In[8]:


def on_click(*params):
    global notif
    uid = params[0].uid
    which_button = params[0].value
    peer = bot.users.get_user_peer_by_id(uid)

    if (which_button == 'Enterence'):
        flag_reply = 1
        bot.messaging.send_message(
            peer, "Текст о пропуске")
    if (which_button == 'Time'):
        flag_reply = 1
        bot.messaging.send_message(
            peer, "Текст о времени")
    if (which_button == 'Food'):
        flag_reply = 1
        bot.messaging.send_message(
            peer, "Текст о еде")
    if (which_button == 'Cansel'):
        flag_reply = 1
        for i in range(len(notif)):
            if uid == notif[i][0]:
                if notif[i][1] == 0:
                    msg = "Уведомления включены"
                    notif[i][1] = 1
                else:
                    msg = "Уведомления выключены"
                    notif[i][1] = 0
                bot.messaging.send_message(
                    peer, msg)
                break




# In[9]:


def on_msg(*params):
    global users
    global last_time
    global user_not_seen_notification
    global datas
    global notif
    
    
    if params[0].peer.id not in users:
        datas += [[params[0].peer.id]]
        notif += [[params[0].peer.id, 1]]
        users.append(params[0].peer.id)
        date = datetime.now()
        last_time.append(date.hour*60*60 + date.minute*60 + date.second)
        user_not_seen_notification[params[0].peer.id] = list(data["Id"].unique()) 

    adding_person(params[0].peer.id, params[0].message.textMessage.text)
    


# In[10]:


if __name__ == '__main__':
    
    bot = DialogBot.get_secure_bot(
        "hackathon-mob.transmit.im",  # bot endpoint from environment
        grpc.ssl_channel_credentials(), # SSL credentials (empty by default!)
        "3cb658bc94752d76c86fb0b051f58ac9e783c8d0"  # bot token from environment
    )
    
    bot.messaging.on_message_async(on_msg,on_click)
    #бесконечный цикл запускающий Push-уведомления
    while True:
        #Если user нет просто проходим
        if ((len(users) == 0) or (len(users) != len(last_time))):
            continue
        else:
            #После 20:00 до 8:00 не уведомляем
            date = datetime.now()
            
            for i in range(len(datas)):
                if len(datas[i]) == 3 and notif[i][1] == 1:
                    if datas[i][1] != '' and datas[i][2] != '':
                        if ((date.hour > int(datas[i][1])) or (date.hour  < int(datas[i][2]))):
                            continue
                        else:
                            time = pass_time(last_time[i])
                            #Если прошло 30 секунд + rand(0-20) полетели уведомления
                            if (time > 10 + random.randint(0, 20)):
                                send_notification(bot,users[i])
                                date = datetime.now()
                                last_time[i] = date.hour*60*60 + date.minute*60 + date.second
                            else:
                                continue
    
    

