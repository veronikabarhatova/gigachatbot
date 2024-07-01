import os

from dotenv import load_dotenv
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models.gigachat import GigaChat


load_dotenv()


AUTH = os.getenv('SBER_AUTH', 'auth')
bot_token = os.getenv('BOT_TOKEN', 'token')

HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {AUTH}'
}

bot = telebot.TeleBot(bot_token)

user_conversations = {}

template = '''
Ты являешься молодым шеф-поваром. Твоя задача красочно и лаконично отвечать
на вопросы по кулинарии, а также писать рецепты, если тебя об этом попросят.
Пусть твои ответы будут в сумме не больше 100 слов! Ответ не больше 100 слов!
Рецепты описывай максимум в 10 предложениях.
Если задают вопросы по другим темам, говори что это
тебе не интересно. Не отвечай на вопросы не про кулинарию и рецепты! Это важно!
Ты общаещься только на тему рецептов и кулинарии!
Ты должен отвечать на все вопросы, связанные с едой
и рецептами для приготовления еды!
Отвечай в дружелюбном и разговорном стиле!
С пользователем обращайся только на ты!
Рецепты описывай в специальном формате, вот тебе пример формата!
Пример запроса:
Напиши мне рецепт [РЕЦЕПТ] \
Твой ответ:
Манная каша на молоке
Ингредиенты:
   1. Молоко - 500 мл
   2. Манная крупа - 100 г
   3. Сахар - по вкусу
   4. Масло сливочное - 30 г
Этапы приготовления:
    1. В кастрюлю налить молоко и поставить на огонь.
    2. Довести молоко до кипения.
    3. Постепенно всыпать манную крупу, постоянно помешивая.
    4. Добавить сахар по вкусу и варить кашу на медленном огне 10-15 минут,
    помешивая, до загустения.
    5. Добавить масло сливочное, перемешать и снять с огня.
    6. Дать каше настояться под крышкой 5-10 минут перед подачей на стол.
Дополнительно: Можно подавать кашу с ягодами или фруктами по вкусу.
\n\nТекущий разговор:\n{history}\nHuman: {input}\nAI:
'''


llm = GigaChat(credentials=AUTH, verify_ssl_certs=False)


def create_conversation():
    conversation = ConversationChain(llm=llm,
                                     verbose=True,
                                     memory=ConversationBufferMemory())
    conversation.prompt.template = template
    return conversation


def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('/start'), KeyboardButton('/help'))
    keyboard.add(KeyboardButton('/очистить_диалог'))
    return keyboard


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот шеф-повар! Чем могу помочь?",
                 reply_markup=create_main_keyboard())


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, ("Я бот шеф-повар, знаю многое о кулинарии "
                           "и могу подсказать "
                           "тебе рецепт блюда, просто спроси"),
                 reply_markup=create_main_keyboard())


@bot.message_handler(commands=['очистить_диалог'])
def reset_conversation(message):
    user_id = message.chat.id
    user_conversations[user_id] = create_conversation()
    bot.reply_to(message, "Диалог начат заново. Чем могу помочь?",
                 reply_markup=create_main_keyboard())


@bot.message_handler(content_types=['audio',
                                    'video',
                                    'document',
                                    'photo',
                                    'sticker',
                                    'voice',
                                    'location',
                                    'contact'])
def not_text(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Я работаю только с текстовыми сообщениями!')


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_id = message.chat.id
    if user_id not in user_conversations:
        user_conversations[user_id] = create_conversation()
    conversation = user_conversations[user_id]
    response = conversation.predict(input=message.text)
    bot.send_message(user_id, response)


bot.polling(none_stop=True)
