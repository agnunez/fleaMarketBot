import time

lastTime = 0

def stilli(bot, update):
    global lastTime
    current_time = time.time()
    if (current_time - lastTime) > 3000: #don't joke too often
        lastTime = current_time
        update.message.reply_text('joke!(c) :)')
