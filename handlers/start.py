from handlers.system import silence_keeper


@silence_keeper
def start(bot, update):
#def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hi! I am a fleaMarketbot!\n Type /help to find out about my capabilities.')