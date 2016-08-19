from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import logging
import signal

import morejpeg

class Bot:
    token = open('token.txt', 'r').read().strip()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    api_url = "https://api.telegram.org"
    bot_url = api_url + "/bot" + token
    
    def __init__(self):
        signal.signal(signal.SIGINT, self.stop)

        self.dispatcher.add_handler(CommandHandler('morejpeg', morejpeg.morejpeg(self)))
        self.updater.start_polling()

    def getFile(self, file_id):
        url = self.bot_url + "/getFile"
        info = requests.post(url, data={ "file_id": file_id }).json()
        path = info["result"]["file_path"]

        url = self.api_url + "/file/bot" + self.token + "/" + path
        return requests.get(url).content

    def sendPhoto(self, content, chat_id):
        url = self.bot_url + "/sendPhoto"
        data = {"chat_id": chat_id}
        files = {"photo": ("a.jpg", content)}
        response = requests.post(url, data = data, files = files)

    def stop(self, signal, frame):
        print("HALTING - Recieved SIGINT")
        self.updater.stop()

bot = Bot()
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
