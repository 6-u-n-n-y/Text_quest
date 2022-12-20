import json
import telebot
from telebot import types


def get_api_token():
    return json.load(open('Json/config.json'))['token']


def get_db():
    return json.load(open('Json/data.json'))


def change_pos(user_id, x):
    with open("peak.json", "rt", encoding="utf-8") as file:
        f = json.load(file)
    f[user_id] = x
    with open("peak.json", "wt", encoding="utf-8") as _file:
        json.dump(f, _file, indent=2)


def get_peak(user_id):
    with open("peak.json", "rt") as f:
        x = json.load(f)
        return x[user_id]


def add_id(user_id):
    with open("peak.json", "rt", encoding="utf-8") as file:
        t = json.load(file)
    t[user_id] = 1
    with open("peak.json", "wt", encoding="utf-8") as f:
        json.dump(t, f, indent=2)
        

token = get_api_token()
bot = telebot.TeleBot(token)
data = get_db()


@bot.message_handler(commands=["start"])
def responce(message):
    add_id(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Поздороваться еще раз и рассказать предысторию")
    btn2 = types.KeyboardButton("Куда я могу пройти?")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Приветствую вас в нашем уникальном текстовом квесте (таких нет ни у кого, мы первые придумали эту идею)', reply_markup=markup)
    

@bot.message_handler(content_types=['text'])
def responce(message):
    user_id = str(message.chat.id)
    can_i_go = False

    if message.text == "Поздороваться еще раз и рассказать предысторию":
        bot.send_message(message.chat.id, "   Еще раз здравствуйте, пришло время узнать, что же с вами произошло.... \n    Прошло несколько лет с того момента, как многие начали замечать крайне странные изменения погоды в вашем городе. Всё начиналось несерьёзно: средняя годовая температура месяц за месяцем уменьшалась и лишь кучка учёных пыталась наводить панику, заявляя о глобальном похолодании. Ну глупость же несусветная, верно?.. Как оказалось - нет. Всё случилось неожиданно. Очередная зима наступила слишком рано. \n    Посевы не взошли, животные начали умирать. Уже в ноябре погода встретила обитателей температурой ниже сорокаградусов. Снег выпал слоем в несколько метров и в итоге условия жизни снизились до уровня угрожающего жизни. Ни провидцы, ни учёные не давали каких-либо хороших прогнозов. По итогу региональным управлением было принято решение о немедленной эвакуации поселения, в том числе и вас.\n    Уже несколько дней вы находитесь в повозке, за окном метель. Стук колёс слился с голосом матери, которая успокаивает ребёнка; множество молитв, которые питают страх перед неизвестностью. Всё стало будто белым шумом. Даже сопровождение военными силами не внушает спокойствия. Наконец вереница беженцев прекратила своё движение. Вам приказали выйти. Вы один из первых в рядах. Солдат приказывает вам пройти за ним. Вас выводят на площадь.")

    elif message.text == "Куда я могу пройти?":
        bot.send_message(message.chat.id, f'Сейчас вы можете: {data[get_peak(user_id)-1][0]["info"]} введите номер действия -> {data[get_peak(user_id)-1][0]["peaks_i_can_reach"]}')

    elif message.text == 'r':
            change_pos(user_id, 1)
            bot.send_message(message.chat.id, "Вы успешно перезапустили игру")
    elif str.isnumeric(message.text):
        peak_to_go = int(message.text)

        if peak_to_go <= len(data):
            splitted = data[get_peak(user_id) - 1][0]["peaks_i_can_reach"].split()
            for i in range(len(splitted)):
                if peak_to_go == int(splitted[i]):
                    can_i_go = True

            if can_i_go:
                change_pos(user_id, peak_to_go)
                bot.send_message(message.chat.id, data[get_peak(user_id)-1][1]["infoaboutplace"])

            else:
                bot.send_message(message.chat.id, "Вы не можете попасть на данный этап") 
                
        else:
            bot.send_message(message.chat.id, "Вы не можете попасть на данный этап")
    

if __name__ == '__main__':
    bot.infinity_polling()
