
# Smart-polling-backend


Smart-polling-backend need two things in order to work:
- Connection to your postgress DB
- Telegram-bot TOKEN

Both are updated in the properties file.

### Connection to your postgress DB
Create a new DB and just put the url like this:
postgresql://{PG-USER-NAME}:{PG-USER-PASSWORD}@{HOST}:{PORT}/{DB-NAME}

property: database.db_url

### Telegram-bot TOKEN
Just take the token you kept when creating the bot and put it in the properties file

property: telegram_bot_token
