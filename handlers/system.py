from config import silent_chats


def silence_keeper(function):
    def wrapper(bot, update, **kwargs):
        if update.message.chat_id in silent_chats:
            return update.message.reply_text('Write me PM, please.')

        return function(bot, update, **kwargs)

    return wrapper
