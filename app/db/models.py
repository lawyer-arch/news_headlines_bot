users:
id
telegram_id
username
created_at

news_sources
id
name
url
is_active

Пример:

1 Bloomberg
2 Kommersant
3 Reuters
4 Vedomosti


news
id
title
url
source_id
published_at
created_at

Важно:

новости должны браться из БД, а не с сайта при запросе пользователя.

subscriptions
id
user_id
source_id
created_at


user_settings
id
user_id
default_source_id
news_limit