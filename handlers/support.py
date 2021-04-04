from handlers.system import silence_keeper


@silence_keeper
def support(bot, update):
    update.message.reply_text(
        'If u want to contribute, write me in telelegram at:\n\n'
        '@agnuca - Agustin Nunez\n'
        'or pullrequest at:\n'
        'https://github.com/agnunez/fleaMarketBot\n'
    )
