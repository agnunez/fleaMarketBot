#!/usr/bin/python3
# -*- coding: utf-8 -*-
import telegram

from db import database
from handlers.system import silence_keeper


@silence_keeper
def all(bot, update):
    items = database().item.get()
    if len(items) == 0:
        update.message.reply_text('There are no products.')
        return

    send_items(update, items)


@silence_keeper
def my_items(bot, update):
    items = database().item.get(userID=update.message.from_user.id)
    if len(items) == 0:
        update.message.reply_text("You don't have any products. Type /add to add")
        return

    send_items(update, items)


def send_items(update, items):
    result = []
    for item in items:
        result.append('%s: %s - %s' % ('/view%s' % item.id, item.decorator().get_title(), item.decorator().get_user()))

    update.message.reply_text('\n'.join(result))
