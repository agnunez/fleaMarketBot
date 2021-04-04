from handlers.system import silence_keeper


@silence_keeper
def support(bot, update):
    update.message.reply_text(
        'If we are doing something wrong, or you have you have suggestion to make it better, write to us.:\n\n'
        '@lnx13 - Михаил "Lynxie" Чичков\n'
        '@d_naumenko - Дмитрий Науменко\n'
    )
