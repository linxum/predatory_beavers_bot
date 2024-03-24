# Predatory Beavers Bot

Этот репозиторий содержит код для бота студенческого киберспортивного клуба Воронежского государственного университета (ВГУ). Бот предназначен для организации событий, управления участниками и облегчения коммуникации внутри клуба.

## Особенности

* Организация и анонсирование предстоящих киберспортивных соревнований.
* Регистрация участников и команд.
* Отслеживание результатов и обновление рейтинга.
* Взаимодействие с участниками через Discord или другие платформы.
* Автоматизация рутинных задач администрирования клуба.

## Начало работы

Чтобы развернуть бота на вашем сервере, выполните следующие шаги:

### Предварительные условия

Убедитесь, что у вас установлены:

- Python 3.8 или выше
- pip для установки зависимостей

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/linxum/predatory_beavers_bot.git
   cd predatory_beavers_bot
   ```
2. Установите зависимости:
  ```bash
  pip install -r requirements.txt
  ```
3. Создайте файл tokens.py в директории src и в нем вставьте следующую функцию со своим токеном:
  ```python
  def tg_token():
    return '<YOUR TOKEN>'
   ```
4. Запустите бота:
  ```bash
  python main.py
  ```
# Использование
Опишите, как использовать бота, включая доступные команды и их описание.

# Поддержка
Если вам нравится этот проект, вы можете поддержать нас звездочкой на GitHub.
