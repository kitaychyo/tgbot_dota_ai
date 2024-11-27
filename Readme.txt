Cоздайте новый проект в PyCharm
Скачайте файлы проекта с Github https://github.com/kitaychyo/tgbot_dota_ai
Перекиньте эти файлы в папку с созданным проектом
Скачайте и установите библиотеки pyarrow, telebot, spacy, scikit-learn, psycopg2, atexit, numpy, pandas, joblib

также необходимо уставновить языковой пакет для spacy
python -m spacy download ru_core_news_sm

Необходимо заменить токен тг бота в файле bot.py в 20 строке на свой токен
В файле db_handler.py необходимо заменить данные на свои данные для работы с БД

Для работы программы необходима PostgreSql