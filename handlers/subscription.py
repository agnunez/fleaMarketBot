import time

from db import database
from handlers.system import silence_keeper
from models.Subscription import Subscription
from log import *


@silence_keeper
def activate(bot, update):
    chatID = update.message.chat_id

    if database().subscription.get(chatID=chatID, all=False):
        update.message.reply_text('The subscription is already active. Say /unsubscribe to unsubscribe')
        return

    subscription = Subscription(chatID)
    database().subscription.save(subscription)
    update.message.reply_text('Subscription enabled, you will receive notes with offers from other members'
                              'in this chat and you can pick up the cool thing first!'
                              '\n\ntype /unsuscribe if you want to stop further notifications.')


@silence_keeper
def deactivate(bot, update):
    chatID = update.message.chat_id

    subscription = database().subscription.get(chatID=chatID, all=False)
    if not subscription: update.message.reply_text("Sorry, you are not signed yet")

    database().subscription.unsubscribe(chatID)
    update.message.reply_text('Subscription cancelled. Hope you found it interesting!'
                              '\n\nPlease, comment your suggestions, will be taken into account :)')


class Notifier:
    """
    Sends notifications to the subscribed users
    """

    def __init__(self, bot, item, rate_per_second=20):
        """

        :type item: models.Item.Item
        :type bot: telegram.bot.Bot
        """
        self.bot = bot
        self.item = item
        self.rate_per_second = rate_per_second

    def run(self):
        subscribers = self.get_subscribers()
        self.spam(subscribers)

    def get_subscribers(self):
        return database().subscription.get()

    def spam(self, subscribers):
        count = 0
        item = self.item
        bot = self.bot

        for subscriber in subscribers:
            count += 1
            if count % self.rate_per_second == 0: time.sleep(1)
            logger.info("Try send messege to subscriber {}".format(subscriber.chatID))
            try:
                if item.get_photo():
                    if item.decorator().is_info_short():
                        bot.send_photo(subscriber.chatID, item.get_photo(), caption=item.decorator().get_info(separator='\n'))
                        continue
                    bot.send_photo(subscriber.chatID, item.get_photo())

                bot.send_message(subscriber.chatID, item.decorator().get_info(separator='\n'))
            except:
                logger.error("messege to subscriber {} doesnt sent".format(subscriber.chatID))
