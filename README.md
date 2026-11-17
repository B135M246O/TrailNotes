# TrailNotes

Сообщество путешественников с путевыми заметками, фотографиями и обсуждениями поездок.
Заметки можно объединять в сообщества по маршруту или виду путешествия.
Участники регистрируются, меняют пароль, публикуют и редактируют собственные заметки,
комментируют записи и подписываются на других путешественников.
Есть общая лента, страницы сообществ и авторов, отдельная лента подписок, пагинация и кеш общей ленты.

Стек: Python 3.11, Django 4.2, SQLite, шаблоны Django, Bootstrap, Pillow и sorl-thumbnail.

## Запуск в PowerShell

Из каталога TrailNotes:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Замените `SECRET_KEY` в `.env` случайным значением. Его можно создать командой
`.\.venv\Scripts\python.exe -c "from secrets import token_urlsafe; print(token_urlsafe(48))"`.
`DEBUG=true` используется для локальной разработки; `ALLOWED_HOSTS` содержит только локальные адреса.

```powershell
.\.venv\Scripts\python.exe yatube\manage.py migrate
.\.venv\Scripts\python.exe yatube\manage.py loaddata travel_communities
.\.venv\Scripts\python.exe yatube\manage.py createsuperuser
.\.venv\Scripts\python.exe yatube\manage.py runserver 127.0.0.1:8003
```

Сайт: http://127.0.0.1:8003/; администрирование: http://127.0.0.1:8003/admin/.
На сайте создайте учётную запись, добавьте заметку с маршрутом и впечатлениями,
выберите сообщество и при желании приложите фотографию. На странице другого путешественника можно подписаться на его заметки.
Fixture добавляет только три тематических сообщества, без чужих учётных записей или паролей.

SQLite находится в `yatube/db.sqlite3`, фотографии — в `yatube/media/`.
Письма восстановления пароля сохраняются в `yatube/sent_emails/`, внешняя почта не нужна.
Без постоянного `SECRET_KEY` сессии инвалидируются при перезапуске.
Имена Python-пакета `yatube`, моделей `Post`/`Group` и URL сохранены для совместимости маршрутов и миграций.

## Проверки

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe yatube\manage.py test about posts users
.\.venv\Scripts\python.exe yatube\manage.py check
.\.venv\Scripts\python.exe yatube\manage.py makemigrations --check --dry-run
```

Существующие проверки публикаций, изображений, комментариев, подписок, доступа, кеширования и пагинации сохранены.
Дополнительные тесты проверяют тематические формы и загрузку демоданных.
Подробности проверки и ограничения — в `REVIEW.md`.

Автор адаптации и доработок — Рябуха Олег.
Сведения об отсутствии отдельной лицензии — в `NOTICE.md`.
