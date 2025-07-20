# 🤡 Telegram Auto Reaction

[![Top Language](https://img.shields.io/github/languages/top/shawtyknowmyname/telegram_auto_reaction)](https://github.com/shawtyknowmyname/telegram_auto_reaction)
[![License](https://img.shields.io/github/license/shawtyknowmyname/telegram_auto_reaction)](https://github.com/shawtyknowmyname/telegram_auto_reaction/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/shawtyknowmyname/telegram_auto_reaction)](https://github.com/shawtyknowmyname/telegram_auto_reaction/stargazers)
[![Downloads](https://img.shields.io/github/downloads/shawtyknowmyname/telegram_auto_reaction/total)](https://github.com/shawtyknowmyname/telegram_auto_reaction/releases)
[![Issues](https://img.shields.io/github/issues/shawtyknowmyname/telegram_auto_reaction)](https://github.com/shawtyknowmyname/telegram_auto_reaction/issues)

## Если вы посчитаете этот проект полезным — поставьте :star: этому репо

**Telegram Auto Reaction** — это десктопное Python-приложение с графическим интерфейсом (PyQt5), которое автоматически ставит реакции (эмодзи) на входящие сообщения в Telegram от вашего имени. Оно использует [Pyrogram](https://docs.pyrogram.org/) и [Telegram API](https://core.telegram.org/api) для работы.

## 🚀 Возможности

- 🔐 Авторизация через Telegram API (API ID + HASH + номер телефона)
- 📂 Локальное хранение сессии в `sessions/`
- 💬 Реакции на сообщения:
  - В ЛС: всем или только избранным пользователям
  - В группах: всем или только избранным участникам
- 👤 Реакция на **собственные** сообщения в группах (опционально)
- ❤️ Реакция по умолчанию и **кастомные реакции** (user:emoji)
- 📊 Логирование в консоль
- 🖱️ Удобный интерфейс на PyQt5
- 🧠 Конфигурация сохраняется в `sessions/config.json`

---

## 📦 Установка

1. Установите Python 3.8–3.12
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/shawtyknowmyname/telegram_auto_reaction.git
   cd telegram_auto_reaction
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите GUI:
   ```bash
   python gui_app.py
   ```

---

## 🧰 Зависимости

Файл `requirements.txt` содержит всё необходимое:
```txt
pyrogram
tgcrypto
PyQt5
```

---

## 🖼️ Интерфейс

При первом запуске:
- **API ID и API HASH** — можно получить на [my.telegram.org](https://my.telegram.org/auth):

> 🔑 **Как получить:**
> 1. Авторизуйтесь на сайте [my.telegram.org](https://my.telegram.org/auth) с помощью вашего номера Telegram и кода подтверждения.
> 2. Перейдите в раздел **API development tools**.
> 3. Заполните форму:
>     - **App title** — произвольное название, например: `AutoReaction`
>     - **Short name** — короткое имя латиницей, например: `autoreact`
>     - **URL** — можно оставить пустым или указать любую ссылку, например: `https://example.com`
>     - **Platform** — выберите `Desktop`
>     - **Description** — можно оставить пустым или указать краткое описание
> 4. Нажмите **Create application**
> 5. Скопируйте выданные **API ID** и **API HASH**

- **Session name** — произвольное имя вашей сессии (например, `clown`)
- **Phone number** — номер Telegram к которому привязан аккаунт, Telegram запросит код подтверждения
- После успешного входа откроется окно доступа к меню настроек

![](https://i.ibb.co/Lzs07xvL/image.png)

Настройки:
- 🔘 Выбор режима реакции в ЛС / группах
- 📜 Список пользователей
- ✅ Чекбокс реакции на **свои** сообщения
- ❤️ Выбор стандартного или кастомного эмодзи
- 📝 Таблица кастомных реакций (`username:emoji`)

![](https://i.ibb.co/h1TbxhN6/123.jpg)

---

## ⚙️ Конфигурация

- `sessions/config.json` — настройки (режимы, пользователи, emoji)
- `sessions/reactions.json` — кастомные реакции
- `sessions/<session_name>.session` — сессия Telegram

---

## 🧾 Структура проекта

```
telegram_auto_reaction/
│
├── auth_window.py        # окно авторизации
├── config_manager.py     # работа с конфигурацией (config.json / reactions.json)
├── gui_app.py            # точка входа, переключение окон
├── main_window.py        # основное окно с настройками
├── reactor_thread.py     # Telegram-клиент с логикой реакций
├── requirements.txt      # зависимости
└── README.md             # этот файл
```

---

## 💡 Примечания

- Используется **userbot**-режим через Pyrogram (вход как пользователь, не бот)
- При смене session name — создаётся новая сессия
- Поддержка unicode-эмодзи (например `🤡`, `❤️`, `🔥` и т.п.)

---

## 📜 Лицензия

[MIT License](https://github.com/shawtyknowmyname/telegram_auto_reaction/blob/main/LICENSE).
