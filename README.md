# fleaMarketBot
Telegram flea market bot for Ukraine FPV group

Bot framework https://github.com/python-telegram-bot/python-telegram-bot

# How to start

## Environment

Create `db.py`:


```python
# Telegram API token. talk to @BotFather to get
token = 'XXXXXXXXXX:ABCABCABCABCABCABCABCABC'# change this to the token you get from @BotFather

# DSN string for connecting to database
db = 'sqlite:///fleaMarket.db' # create this database with ... $ sqlite3 fleaMarket.db in same project directory

# List of chat IDs in which the bot will always offer to communicate in LAN
silent_chats = ["-XXXXXXXX"] # can be a @username or a ids 
```

## Register bot commands in BotFather

```
/setcommands

help - show this message 
list - show a list of product names that are currently on sale
subscribe - subscribe to new products newsletter
unsubscribe - unsuscribe from the newsletter of new products
add - add your product
edit - edit your product
delete - delete your product
support - ask for support
...


# Roadmap

  - Regular check of relevance
  - Improve post design, possibly apply Markdown
  - Banlist

# Translations

- English @agnuca, github.com/agnunez/fleaMarketBot

# Python-Telegram-Bot 

- 20210404 Bot API 5.1 updated by @agnuca to get working bot