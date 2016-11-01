#Ligar esse script quando o outro script estiver fora do ar.
#BOT MAINTENANCE -- created by Pedro Pereira -- IME - USP

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram.error import TelegramError, Unauthorized, BadRequest, TimedOut, NetworkError
import logging

#Logging setup
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

#Updater and dispatcher
BCCToken = '231639389:AAGPgwwzeOrL45gArbdfzvH3VH2uD2WVuqE'

updater = Updater(token = BCCToken)
dispatcher = updater.dispatcher

#Bot functions

def start(bot, update):
	bot.sentMessage(chat_id = update.message.chat_id,
		text = '_OLAR!_ Sou o *BotCC*.\n\nInfelizmente, estou em manutenção no momento. Por favor falar com @pedro823 para que ele consiga me por de volta no ar o mais rápido possível. Obrigado!',
		parse_mode = ParseMode.MARKDOWN)

def unknown(bot, update):
	bot.sendMessage(chat_id = update.message.chat_id,
		text = 'Perdão! Estou em manutenção no momento. @pedro823, o que tá acontecendo comigo?')

#Handlers
start_handler = CommandHandler('start', start)
unknown_handler = MessageHandler([Filters.command], unknown)

#Add to dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(unknown_handler)

#Start bot
updater.start_polling()
print("Bot is in maintenance mode now.")
