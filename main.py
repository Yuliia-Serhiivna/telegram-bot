import telebot
import json

print('init')
bot = telebot.TeleBot("979731314:AAFZ1FX8egsAu5T0O2jdEY-4iQbd9iGehYM") #750756493:AAE2pCVH2q-kW5Hwsk7CbrUT23SgFr6y_7o")
chat_context = {}
chat_state = {}


@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi. Where are you want to going?")
    bot.send_message(message.chat.id, "Choose the country")
    chat_state[message.chat.id] = 'ask_country'

@bot.message_handler(content_types = ['text'])
def message_handler(message):
    if not message.chat.id in chat_state:
        chat_state[message.chat.id] = 'ask_country'
        chat_context[message.chat.id] = {}
    state = chat_state[message.chat.id]
    context = chat_context[message.chat.id]
    if state == 'ask_country':
        with open(r'countries.json', 'r') as JSON:
            json_dict = json.load(JSON)
            if json_dict.get(message.text):
                bot.reply_to(message, "Great! What city?")
                context['country'] = message.text
                print(context['country'])
                state = 'ask_city'
                print(json_dict.get(context['country']))
            else:
                bot.reply_to(message, "Sorry. Can't found that country. ")
    elif state == 'ask_city':
        with open(r'countries.json', 'r') as JSON:
            json_dict = json.load(JSON)
        if message.text in json_dict.get(context['country']):
            bot.reply_to(message, "Great! What day?")
            context['city'] = message.text
            state = 'ask_day'
        else:
            bot.reply_to(message, "Sorry. Can't found that city. ") 
    elif state == 'ask_day': ### ask the day
        if message.text.isdigit() and int(message.text) >= 1 and  int(message.text) <= 31:
            context['day'] = message.text
            state = 'ask_room'
            bot.reply_to(message, "What month?")
        else:
            bot.reply_to(message, "Wrong day :(")
    elif state == 'ask_room': ### ask the day
        if message.text.isdigit() and  int(message.text) >=1 and int(message.text) <= 12:
             context['month'] = message.text
             state = 'say_ok'
             bot.reply_to(message, "What kind of room(single,double,king)?")
        else:
             bot.reply_to(message, "Wrong day :(")
    elif state == 'say_ok': ### ask the month
        if message.text in ['single','double','king']:
            context['room'] = message.text
            bot.reply_to(message, "Ok, I will book a " + context['room'] + " room in " + context["country"] + " " + context["city"] + " at " + context["day"] + "/" + context["month"] )
            state = 'ask_country'
            chat_context[message.chat.id] = {}
        else:
            bot.reply_to(message, "Wrong room type.")



    chat_state[message.chat.id] = state

if __name__ == '__main__':
    print('polling')
    bot.polling(none_stop = True)