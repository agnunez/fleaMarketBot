#!/usr/bin/env python
# -*- coding: utf-8 -*-


from db import database
from handlers.system import silence_keeper


@silence_keeper
def delete_item(bot, update, groups):
    # todo: спросить, уверен ли
    id = groups[0]
    item = database().item.get(id=id, userID=update.message.from_user.id, all=False)
    if item is None:
        update.message.reply_text('Product with ID "%s" not found' % id)
        return

    item.is_active = False
    update.message.reply_text('Item "%s" has been deleted' % item.decorator().get_title())
    database().item.save(item)


@silence_keeper
def list_items(bot, update):
    items = database().item.get(userID=update.message.from_user.id)
    if len(items) == 0:
        update.message.reply_text('You have no active items. Do you want to create one? Type /add')
        return

    send_items(update, items)


def send_items(update, items):
    result = []
    for item in items:
        result.append('%s: %s' % ('/delete%s' % item.id, item.decorator().get_title()))

    update.message.reply_text('\n'.join(result))
