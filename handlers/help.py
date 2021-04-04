from handlers.system import silence_keeper


@silence_keeper
def help(bot, update):
    update.message.reply_text(
        '/ help - show this message\n'
        '/ list - show a list of product names that are currently on sale\n'
        '/ subscribe - subscribe to new products\n'
        '/ unsubscribe - unsubscribe from mailing of new products\n'
        '/ add - add your product\n'
        '/ edit - edit your product\n'
        '/ delete - delete your product\n'
        '/ support - ask for support\n'        
    )
