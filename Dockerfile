# Используем Python 3.11 как базовый образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app/

# Копируем файлы проекта в контейнер
COPY bot/ /usr/src/app/

# Копируем файл базы данных
COPY bot/cfg/database.db /usr/src/app/bot/cfg/database.db

# Устанавливаем зависимости
COPY req.txt ./
RUN pip install -r req.txt

# Запуск бота
CMD ["python", "bot/bot_main.py"]
