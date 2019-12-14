import telebot
import json
import requests
import time
from telebot import types

TOKEN = "933287638:AAHZSQ3f7UZDY8ZrbwzttjR0NbtwaVepg_Y"

with open('response.json') as f:
    response = json.load(f)

with open('dict.json') as f2:
	dic = json.load(f2)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Type /start to have see events\nType \'player\' to see stats")

#chat_id = bot.get_updates()[-1].message.chat.id

#@bot.message_handler(func=lambda message: True)
@bot.message_handler(regexp="player")
def handle_message(message):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, selective=False)
	for i in range(10):
		markup.add(types.KeyboardButton(str(i)))
	bot.send_message(message.chat.id, "Choose a player:", reply_markup=markup)
	@bot.message_handler(regexp="\d")
	def handle_inner_message(msg):
		player_num =  int(float(msg.text))

		Assists = response["RoundEndState"]["Players"][player_num]["AdditionalInfo"]["Assists"]
		Deaths = response["RoundEndState"]["Players"][player_num]["AdditionalInfo"]["Deaths"]
		Score = response["RoundEndState"]["Players"][player_num]["AdditionalInfo"]["StartScore"]
		Kills = response["RoundEndState"]["Players"][player_num]["AdditionalInfo"]["Kills"]
		MVPs = response["RoundEndState"]["Players"][player_num]["AdditionalInfo"]["MVPs"]
		Money = response["RoundStartState"]["Players"][player_num]["Money"]
		MoneyLeft = response["RoundEndState"]["Players"][player_num]["Money"]
		
		bot.send_message(message.chat.id, "Kills in previous rounds: " + str(Score))
		bot.send_message(message.chat.id, "Kills: " + str(Kills))
		bot.send_message(message.chat.id, "Assists: " + str(Assists))
		bot.send_message(message.chat.id, "Deaths: " + str(Deaths))
		bot.send_message(message.chat.id, "MVPs: " + str(MVPs))
		bot.send_message(message.chat.id, "Money: " + str(Money))
		bot.send_message(message.chat.id, "Money left: " + str(MoneyLeft))


@bot.message_handler(commands=['start'])
def echo_all(message):
	for i in range(0, 2981):
		URL = "http://7a6066b9.ngrok.io/get-event"
		PARAMS = {'frame': i}
		r = requests.get(url = URL, params = PARAMS) 
		data = r.json()
		for j in range(len(data)):
			bot.send_message(message.chat.id, 'FrameNumber: ' + str(data[j]['FrameNumber']) + '\nEventType: ' + dic[str(data[j]['EventType']) if int(data[j]['EventType']) < 67 else '0'])
			# Specify weapon! str(data[j]['Data']['Weapon']
			#bot.send_message(chat_id, 'EventType: ' + dic[str(data[j]['EventType']) if int(data[j]['EventType']) < 67 else '0'])
			print(data[j])
			#if j == 5:
			#	breaks
		time.sleep(2)

bot.polling()