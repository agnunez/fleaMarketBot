#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handlers.system import silence_keeper
from log import *
from db import database
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

# add item conversation
NAME, DESCRIPTION, PHOTO, PUBLISH = range(4)


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
        result.append('%s: %s' % ('/edit%s' % item.id, item.decorator().get_title()))

    update.message.reply_text('\n'.join(result))


@silence_keeper
def edit(bot, update, groups, user_data):
    reply_keyboard = [['/skip', ]]

    id = groups[0]
    item = database().item.get(id=id, userID=update.message.from_user.id, all=False)
    if item is None:
        update.message.reply_text('Product ID "%s"not found' % id)
        return

    user_data['item'] = item
    update.message.reply_text('The message below contains the current name of the product. '
                              'Write a new one, or press /skip to leave it unchanged\n')
    update.message.reply_text(item.itemName,
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  resize_keyboard=True
                              ))

    return NAME


def name(bot, update, user_data):
    """edit item name"""

    item = user_data['item']
    itemName = update.message.text
    logger.info("Change item name: %s" % (itemName))
    item.add_name(itemName)
    skip_name(bot, update, user_data)

    return DESCRIPTION


def skip_name(bot, update, user_data):
    """skip edit item name"""
    reply_keyboard = [['/skip', ]]

    item = user_data['item']
    update.message.reply_text('Excellent! The message below contains the current description. '
                              'Write a new one, or press /skip to leave it unchanged\n')
    update.message.reply_text(item.itemDescription,
                          reply_markup=ReplyKeyboardMarkup(
                              reply_keyboard,
                              one_time_keyboard=True,
                              resize_keyboard=True
                          ))

    return DESCRIPTION


def description(bot, update, user_data):
    """add item description"""
    item = user_data['item']
    itemDescription = update.message.text
    logger.info("Change item description: %s" % (itemDescription))
    item.add_description(itemDescription)
    skip_description(bot, update, user_data)

    return PHOTO


def skip_description(bot, update, user_data):
    """add item description"""
    reply_keyboard = [['/skip', ]]
    item = user_data['item']

    update.message.reply_text('Last step. Send a photo of the product, or click /skip, '
                              'to leave the existing one unchanged.',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  resize_keyboard=True
                              ))

    return PHOTO


def photo(bot, update, user_data):
    """change item photo"""
    item = user_data['item']
    photo_id = update.message.photo[-1].file_id
    logger.info("Change item photo id %s" % (photo_id))
    item.add_photo(photo_id)
    skip_photo(bot, update, user_data)

    return PUBLISH


def skip_photo(bot, update, user_data):
    """if item without photo"""
    pre_publish(bot, update, user_data)

    return PUBLISH


def cancel(bot, update, user_data):
    """interrupt editing"""
    user = update.message.from_user
    del user_data['item']
    logger.info("User %s cancel editing" % (user.first_name,))
    update.message.reply_text('Ok, canceled.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def pre_publish(bot, update, user_data):
    """check item before publish"""
    item = user_data['item']
    reply_keyboard = [['/save', '/cancel', ]]
    update.message.reply_text('Ok?\n' + item.decorator().get_info(separator='\n'),
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  resize_keyboard=True
                              ))


def publish(bot, update, user_data):
    """publish item"""
    item = user_data['item']
    database().item.save(item)
    update.message.reply_text('Item saved!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END