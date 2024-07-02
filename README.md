# Чат-бот для получения рецептов

## Описание
Проект Giga - чат-бот для получения рецептов и ответов на вопросы по кулинарии с интеграцией GigaChat

## Технологии:

- Python 3.9
- pyTelegramBotAPI
- gigachain

## Установка (MacOS):

1. Клонирование репозитория

```
git clone https://github.com/veronikabarhatova/
```

2. Переход в директорию django_sprint4

```
cd 
```

3. Создание виртуального окружения

```
python3 -m venv venv
```

4. Активация виртуального окружения

```
source venv/bin/activate
```

5. Обновите pip

```
python3 -m pip install --upgrade pip
```

6. Установка зависимостей

```
pip install -r requirements.txt

```

7. Получение токена у BotFather для чат-бота

```

- Найдите в Telegram аккаунт @BotFather.
- Напишите ему команду /newbot.
- Следуйте инструкциям BotFather для выбора имени вашего бота.
- После создания бота BotFather предоставит вам токен для доступа к Telegram Bot API.

```

8. Получение доступа к GigaChat API

```

- Регистрируемся на сайте https://developers.sber.ru/studio/login
- Нажмите кнопку Создать проект в левом меню.
- Выберите GigaChat API в разделе AI-модели.
- Для генерации клиентского ключа нажмите кнопку Сгенерировать новый Client Secret.
- В открывшемся окне скопируйте и сохраните значение полей Client Secret и Авторизационные данные.

```

9. Запуск чат-бота

```
python bot.py

```

10. Деактивация виртуального окружения

```
deactivate

```
## Ссылка на чат-бот: 
https://t.me/Giga_Chat_help_bot
