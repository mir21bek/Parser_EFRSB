from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_a_reply():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Спарсить")

    keyboard_builder.button(text="Добавить пользователя")
    keyboard_builder.button(text="Удалить пользователя")
    keyboard_builder.button(text="Список пользователей")
    keyboard_builder.adjust(1, 2, 1)

    return keyboard_builder.as_markup(resize_keyboard=True)


def start_reply():
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text="Спарсить")
    return keyboard_builder.as_markup(resize_keyboard=True)
