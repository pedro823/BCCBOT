'''
		BCC BOT
	By:
	Pedro Pereira (BCC - 2016)
	IME - USP

'''

from telegram import ParseMode, Message, Chat, Emoji
from telegram.ext import Updater, CommandHandler, Filters, JobQueue, MessageHandler
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, NetworkError
import logging
import sys
import datetime
import re

#bot version
versionString = '0.1.0 alpha'


#Logging setup
logFile = 'botlog.txt'

LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR, 'critical': logging.CRITICAL}

logging.basicConfig(filename = logFile, level=logging.INFO)
'''
if len(sys.argv) > 1:
	level_name = sys.argv[1]
	level = LEVELS.get(level_name, logging.NOTSET)
	logging.basicConfig(level=level)
'''
#updater and dispatcher

#CHANGE TOKEN HERE
BCCToken = '231639389:AAGPgwwzeOrL45gArbdfzvH3VH2uD2WVuqE'
alertFile = 'PeopleToAlert.txt'
calFile = 'calProva.txt'

updater = Updater(token = BCCToken)
dispatcher = updater.dispatcher
job_queue = updater.job_queue

#Figure today's date
today = [int(i) for i in str(datetime.date.today()).split('-')]
today.reverse()
today[2] -= 2000


#Auxiliar functions

def validateDate(date):
	try:
		datetime.datetime.strptime(date, '%d-%m-%Y')
		ret = [int(i) for i in date.split('-')]
		ret[2] -= 2000
	except ValueError:
		logging.info("Wrongly parsed/incorrect date: " + date)
		return False
	for i in range(len(ret)-1, -1, -1):
		if ret[i] > today[i]:
			break
		elif ret[i] < today[i]:
			return -1
	return ret

def checkFile(alertfile, name):
	check = open(alertfile, 'r')
	for line in check:
		if line.strip('\n') == name:
			return True
	return False
	check.close()

def appendToFile(alertfile, name):
	check = open(alertfile, 'a')
	temp = check.write(name + '\n')
	if temp == len(name + '\n'):
		return True
	else:
		logging.error("AppendToFile returned false!")
		return False
	check.close()

def removeFromFile(alertfile, name):
	check = open(alertfile, 'r')
	lines = check.readlines()
	finalCheck = []
	flag = False
	for line in lines:
		if line.strip('\n').strip() != name.strip():
			finalCheck.append(line)
		else:
			flag = True
	check.close()
	check = open(alertfile, 'w')
	check.writelines(finalCheck)
	check.close()
	return flag

def readAllFromFile(alertfile):
	check = open(alertfile, 'r')
	lines = check.readlines()
	finalString = ''
	for line in lines:
		finalString = finalString + '@' + line.strip('\n').strip() + ' '
	check.close()
	return finalString

#Bot functions

def start(bot, update):
	# /start -- sends greeting
	bot.sendMessage(chat_id = update.message.chat_id,
		text = "_OLAR!_ Sou o *BotCC*. Digite /help para saber todos os comandos disponíveis. Para alguma reclamação ou sugestão, contate @pedro823.",
		parse_mode = ParseMode.MARKDOWN)
	logging.info("Processed start from " + update.message.from_user.username)

def help(bot, update):
	# /help -- send a help message
	message = update.message.text.split(' ')
	if len(message) == 2:
		pass
	else:
		bot.sendMessage(chat_id = update.message.chat_id,
			text = ("*Comandos Disponíveis:* \n*/help*: Mostra essa mensagem.\n*/callout*: Chama a atenção de todos em um grupo.\n*/seguiralertas*: Se inscreve para a lista de callouts.\n*/sairalertas*: Sai da lista de callouts.\n*/admin*: chama os administradores do grupo.\n*/dev*: chama os desenvolvedores do bot.\n*/version*: mostra a versão que está sendo rodada no bot no momento.\n"),
			parse_mode = ParseMode.MARKDOWN,
			disable_notification = True)
		logging.info("Processed help from " + update.message.from_user.username)

def callout(bot, update):
	# /callout -- calls everyone in group chat
	if update.message.chat.type == 'private':
		bot.sendMessage(chat_id = update.message.chat_id, text = "Esse comando só está disponível em grupos.")
		help(bot, update)
	else:
		callNames = readAllFromFile(alertFile)
		bot.sendMessage(chat_id = update.message.chat_id, text = "Callout emitido por " + update.message.from_user.first_name + '\n' + callNames + str(update.message.text).strip("/callout").strip())
	logging.info("Processed callout from " + update.message.from_user.username)

def version(bot, update):
	bot.sendMessage(chat_id = update.message.chat_id, text = "Version " + versionString, disable_notification = True)
	logging.info("Processed version from " + update.message.from_user.username)

def joinAlerts(bot, update):
	nameCheck = update.message.from_user.username
	if nameCheck == '':
		bot.sendMessage(chat_id = update.message.chat_id, text = "Por favor, configure um @tag pra você antes de chamar esse comando!")
		return False
	if update.message.chat.type == 'private':
		bot.sendMessage(chat_id = update.message.chat_id, text = "Esse comando só funciona no grupo.")
		logging.info(update.message.from_user.username + " Tried joinAlerts on private message.")
		return False
	if checkFile(alertFile, nameCheck):
		bot.sendMessage(chat_id = update.message.chat_id, text = update.message.from_user.first_name + ", você já foi cadastrado(a) aos alertas!", disable_notification = True)
		logging.info("Tried to register " + nameCheck + " but they're already in!")
	else:
		appendToFile(alertFile, nameCheck)
		bot.sendMessage(chat_id = update.message.chat_id, text = "Cadastrado " + nameCheck + "!")
		logging.info("Registered " + nameCheck + " In alertList successfully")
	return True

def admin(bot, update):
	bot.sendMessage(chat_id = update.message.chat_id, text = '@leolana')

def dev(bot, update):
	bot.sendMessage(chat_id = update.message.chat_id, text = '@pedro823')

def barraP(bot, update):
	bot.sendMessage(chat_id = update.message.chat_id, text = '>:)')

def leaveAlerts(bot, update):
	name = update.message.from_user.username
	if removeFromFile(alertFile, name):
		bot.sendMessage(chat_id = update.message.chat_id, text = "Retirei o seu username da lista. Que pena :c", disable_notification = True)
	else:
		bot.sendMessage(chat_id = update.message.chat_id, text = "Você não estava cadastrado(a)!", disable_notification = True)

# def provas(bot, update):
# 	materia = str(update.message.text).strip('/provas').strip()
# 	if materia == '':
# 		usageProvas(bot, update)
# 		return False
# 	calendario = open(calFile)
# 	lines = calendario.readlines()
# 	for i in range(len(lines)):
# 		if '--' in lines[i]:
# 			if message == lines[i].strip('\n').strip()



def unknown(bot, update):
	bot.sendMessage(chat_id = update.message.chat_id, text = "Ãh? não entendi esse comando.", disable_notification = True)
	help(bot, update)
	logging.info("unknown command from " + update.message.from_user.username + ": " + str(update.message.text))


#Handlers for functions

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
callout_handler = CommandHandler('callout', callout)
version_handler = CommandHandler('version', version)
joinAlerts_handler = CommandHandler('seguiralertas', joinAlerts)
leaveAlerts_handler = CommandHandler('sairalertas', leaveAlerts)
admin_handler = CommandHandler('admin', admin)
dev_handler = CommandHandler('dev', dev)
unknown_handler = MessageHandler([Filters.command], unknown)



#Add handlers to dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(callout_handler)
dispatcher.add_handler(version_handler)
dispatcher.add_handler(joinAlerts_handler)
dispatcher.add_handler(leaveAlerts_handler)
dispatcher.add_handler(admin_handler)
dispatcher.add_handler(dev_handler)
dispatcher.add_handler(unknown_handler)
logging.info("Added handlers")

#Start bot
updater.start_polling()
logging.info("Started Polling")

#Print bot info on screen
print("BotCC is now running.\n")
