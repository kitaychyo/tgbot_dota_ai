import telebot
from telebot import types
import dota_ai
import spacy
import text_parser
from db_handler import DBHandler
import atexit

nlp = spacy.load("ru_core_news_sm")

db = DBHandler()

ai = dota_ai.dota_ai()
n = 200
ai.train(n)
mas_hero = ai.df_hero[0].to_list()
user_data = {}
s = '\n'.join(mas_hero[:-1])

bot = telebot.TeleBot('7692907060:AAGSg9M2y1kqfJBCa1TeuWBzF1mbTwrx-Qg')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать использование")
    btn2 = types.KeyboardButton("Помощь")
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Данный бот может использоваться для предсказания матчей по Dota2", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Обрабатывает текстовые сообщения от пользователя."""
    user_input = message.text.lower()
    doc = nlp(user_input)

    db.save_message(message.from_user.id, message.from_user.username, message.text)

    # Распознавание намерений пользователя
    if any(token.lemma_ == "помощь" for token in doc):
        show_help(message)
    elif any(token.lemma_ == "начать" for token in doc):
        start_usage(message)
    elif any(token.lemma_ == "точность" for token in doc):
        bot.send_message(message.from_user.id, f"Точность модели: {ai.accuracy_test_data()}")
    elif any(token.lemma_ == "герой" for token in doc):
        bot.send_message(message.from_user.id, s)
    elif any(token.lemma_ in ["предсказать", "результат"] for token in doc):
        bot.send_message(message.from_user.id, "Введите данные для предсказания результата матча.")
        user_data[message.from_user.id] = 'waiting_for_prediction_data'
    elif user_data.get(message.from_user.id) == 'waiting_for_prediction_data':
        user_input = message.text
        try:
            parsed_data = text_parser.parse_input_text_to_data(user_input)
            bot.send_message(message.from_user.id, f"Данные успешно обработаны")
            prediction = ai.result(parsed_data)
            winner = "Radiant" if prediction == 1 else "Dire"
            bot.send_message(message.from_user.id, f"Предсказание: победит команда {winner}.")
            video_path = 'Но это не точно.mp4'
            bot.send_video(message.from_user.id, open(video_path, 'rb'))
        except Exception as e:
            bot.send_message(message.from_user.id, "Ошибка при обработке данных. Проверьте формат ввода.")
            print(f"Ошибка: {e}")
    else:
        bot.send_message(message.from_user.id, "Извините, я не понял ваш запрос. Попробуйте выбрать действие из меню.")

def show_help(message):
    """Отображает список функций и инструкций по использованию бота."""
    help_text = (
        "⚙️ **Список доступных команд и функций бота**:\n\n"
        "1️⃣ **Вывести точность**\n"
        "   - Узнать текущую точность модели предсказания.\n\n"
        "2️⃣ **Предсказать результат матча**\n"
        "   - Просмотр всех доступных героев в системе.\n\n"
        "   - Введите данные о командах, игроках и героях для прогноза.\n"
        "   - Формат ввода будет показан перед использованием.\n\n"
        "   - Пример входных данных: Команда Radiant: Invincible Warriors. Игроки: Player1 на Luna, Player2 на Rubick, Player3 на Beastmaster, Player4 на Sniper, Player5 на Lich. Команда Dire: Shadow Fiends. Игроки: PlayerA на Mirana, PlayerB на Wraith King, PlayerC на Dark Willow, PlayerD на Ogre Magi, PlayerE на Zeus."
        "3️⃣ **Вывести список героев**\n"
        "❓ Если у вас возникли вопросы, начните ввод текста, и бот попытается понять ваш запрос."
    )
    bot.send_message(message.from_user.id, help_text, parse_mode='Markdown')

def start_usage(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Вывести точность')
    btn2 = types.KeyboardButton('Предсказать результат матча')
    btn3 = types.KeyboardButton('Вывести список героев')
    markup.add(btn1, btn2, btn3)
    bot.send_message(
        message.from_user.id,
        "Выберите одно из доступных действий:",
        reply_markup=markup,
    )
@atexit.register
def close_resources():
    """Закрывает соединения перед завершением работы программы."""
    db.close()

bot.polling(none_stop=True, interval=0)

