import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard  # <===
key = "7af56d1c8a1120445bc93f2b4b4a91c6d2833191274247c31c41c55385bede53c85af6c660c6136aa7137"
# Авторизуемся как сообщество
vk = vk_api.VkApi(token=key)

def send_message(user_id, message, keyboard = None):  # <===
                from random import randint
                vk.method('messages.send', #принимает в качества аргумента:
                          {'user_id': user_id, #id пользователя
                           "random_id":randint(1,1000) , #он поймёт, что это не повтор сообщения
                           'message': message, #сообщения
                           'keyboard':keyboard.get_keyboard() if keyboard else None,}  #отправка клавиатуры
                          )
#клавиатуры:
start_keyboard = VkKeyboard(one_time = True)  # <===
start_keyboard.add_button('START')
start_keyboard.add_line()
start_keyboard.add_button('NOT START')
main_keyboard = VkKeyboard(one_time = True)  # <===
main_keyboard.add_button('Об авторе')
main_keyboard.add_button('Сделать пожертвование')

main_keyboard.add_line()
main_keyboard.add_button('Сыграть в игру')

main_keyboard.add_button('узнать погоду')
back_keyboard = VkKeyboard(one_time = True)
back_keyboard.add_button('Назад')
 
gamers={}
game_over_keyboard = VkKeyboard(one_time = True)
game_over_keyboard.add_button('Выйти')
game_over_keyboard.add_button ()
game_over_keyboard.add_button("Продолжить")

# Работа с сообщениями
"""
longpoll - объект, читающий сообщения.
"""
longpoll = VkLongPoll(vk)
# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня(то есть бота) сообщение пришло к нам-с.
        if event.to_me:
            #неожиданно, тест. lower - опуск на нижний регистр.
            text = event.text.lower()
            #id пользователя
            user_id = event.user_id
            print(text)
            if user_id in gamers:
                try:
                    otvet = int(text)
                except:
                    if text == "выйти":
                    del gamers[user_id]
                    else:
                        send_message(user_id,"ты чё, продолжай играть." game_over_keyboard)
                    continue
                if otvet > gamers[user_id]:
                    send_message(user_id,"mnoga")
                elif otvet < gamers[user_id]:
                    send_message(user_id,"malo")
                else:
                    send_message(user_id,"Победил", main_keyboard)
                    del gamers[user_id]
            else:
                if text == 'START'.lower():   
                    send_message(user_id,"Добро пожаловать",main_keyboard)  # <===
                    
                elif text == 'Об авторе'.lower():   
                    send_message(user_id,"NEDamir",back_keyboard)
                elif text == 'Сделать пожертвование'.lower():   
                    send_message(user_id,"Платежка еще не подключена",back_keyboard)
                elif text == 'Сыграть в игру'.lower():
                    from random import randint
                    gamers[user_id] = randint(1,10000)
                    send_message(user_id,"угадывай до 10000")
                elif text == 'узнать погоду'.lower():   
                    send_message(user_id,"ясно",back_keyboard)
                else:
                    send_message(user_id,"Продолжайте",main_keyboard)
