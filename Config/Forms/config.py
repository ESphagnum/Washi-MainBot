# Form config.py
import json
from config import language

useEmbed = False
locate = f"Lang/Forms/forms_{language}.json"
loc = json.load(open(locate,"r",encoding="utf-8"))

SETTINGS = {
    "command_role": 1327714717468196948,  # Роль, имеющая доступ к командам
    "embed_color": 0x000000,  # Цвет эмбедов (в формате HEX)
    "log_embed_color": 0x0000ff,  # Цвет эмбедов для логов
    "button_label": "Отправить форму",  # Текст кнопки для формы
    "button_style": 1,  # Стиль кнопки (1 - Primary, 2 - Secondary, 3 - Success, 4 - Danger)
    "log_channel_id": 1328257387693604885,  # ID канала для логов
    "ticket_category_id": 1333526017628831867, # ID категории для тикетов
    "db_file": "bot_data.db",
    "GUILD": 1310050065683058829
}

FORMS = {
    "join_ru": {
        "title": "Вступить в клан",
        "description": "**Для вступления в наш клан вам нужно: Прочитать правила и заполнить форму. Не спамьте заявками. Мы обязательно расмотрим вашу заявку.**",
        "image": "https://share.creavite.co/6782b8560ae0e4f686a65b56.gif",
        "embed_color": 0x000000,
        "questions": [
            {
                "type": "text",
                "label": "Ваш профиль на Blazing Front",
                "placeholder": "Введите ссылку на ваш профиль на Blazing Front",
            },
            {
                "type": "text",
                "label": "Название своего чита",
                "placeholder": "NL/FT/NW/Другое",
            },
            {
                "type": "text",
                "label": "Сколько вы готовы общаться в голосовом?",
                "placeholder": "Введите время, которое готовы уделять",
            },
            {
                "type": "text",
                "label": "Придумайте себе новый никнейм",
                "placeholder": "Прилагательное + Заяц",
            }

        ],
    },
    "join_en": {
        "title": "Join the clan",
        "description": "**To join our clan you need to: Read the rules and fill out the form. Don't spam requests. We will definitely consider your application.**",
        "image": "https://share.creavite.co/6782c0de0ae0e4f686a65b78.gif",
        "embed_color": 0x000000,
        "questions": [
            {
                "type": "text",
                "label": "Blazing Front Profile",
                "placeholder": "Url",
            },
            {
                "type": "text",
                "label": "What u using?",
                "placeholder": "NL/FT/NW/Other",
            },
            {
                "type": "text",
                "label": "Your GMT Time",
                "placeholder": "Enter your GMT Time ",
            },
            {
                "type": "text",
                "label": "Make a new nickname for yourself",
                "placeholder": "Adjective + Hare"
            }
        ],
    },
    "support": {
        "title": "Техподдержка",
        "description": "Откройте тикет, чтобы получить помощь от нашей команды.",
        "message": "Пожалуйста, опишите вашу проблему. Нажмите 'Закрыть', чтобы завершить тикет.",
        "close_button": "Закрыть",
        "close_with_reason_button": "Закрыть с причиной",
    }
}
