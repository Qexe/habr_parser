Парсер написан на requests + lxml

Собирает данные со страницы https://career.habr.com/resumes 

Уникальные собранные данные записываются в базу данных

Для запуска необходимо сбилдить Docker контейнеры базы данных и самого парсера и поднять их

Билдим и поднимаем контейнеры. Команды вводить на одном уровне с файлами docker-compose.yml и Dockerfile.

```docker-compose build```

```docker-compose up```

Чтобы запустить скрипт:

Заходим в контейнер habr_parser:

```docker exec -it <id контейнера> /bin/bash```

Далле вводим команды в терминале контейнера:

```cd app```

```python habr_parser.py```
