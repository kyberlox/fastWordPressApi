# Универсальный шаблон WordPress + FastAPI

Этот шаблон предоставляет готовую инфраструктуру для разработки веб-приложений, где WordPress используется как фронтенд (CMS и управление контентом), а FastAPI — как бэкенд (REST API для кастомной логики, микросервисов, интеграций).

## Структура проекта

```
.
├── api/                    # FastAPI приложение
│   ├── main.py            # Точка входа FastAPI
│   ├── requirements.txt   # Зависимости Python
│   ├── Dockerfile         # Контейнеризация FastAPI
│   ├── database/          # Модели и подключение к БД
│   ├── models/            # SQLAlchemy модели
│   ├── routers/           # Маршруты API
│   ├── schemas/           # Pydantic схемы
│   └── utils/             # Вспомогательные утилиты
├── wordpress/             # Файлы WordPress (volume отключён по умолчанию)
│   ├── wp-config.php      # Конфигурация WordPress
│   ├── wp-content/        # Темы, плагины, загрузки (если volume включён)
│   └── ...                # Остальные файлы WordPress
├── nginx/                 # Конфигурация Nginx
│   └── app.conf           # Виртуальный хост
├── postgresql/            # Данные PostgreSQL (том)
├── docker-compose.yaml    # Оркестрация контейнеров
├── .env.example           # Пример переменных окружения
└── README.md              # Эта документация
```

## Компоненты

1. **PostgreSQL** — база данных для WordPress и FastAPI
2. **FastAPI** — современный асинхронный Python‑фреймворк для API
3. **WordPress** — система управления контентом (фронтенд)
4. **Nginx** — веб‑сервер, проксирующий запросы к WordPress и FastAPI

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git (для клонирования)

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd lemark
   ```

2. Настройте переменные окружения:
   ```bash
   cp .env.example .env
   # Отредактируйте .env при необходимости
   ```

3. Запустите контейнеры:
   ```bash
   docker-compose up -d
   ```

4. Проверьте работоспособность:
   - WordPress: http://localhost:8888
   - FastAPI Swagger: http://localhost:8000/docs
   - FastAPI Health: http://localhost:8000/health
   - Nginx (прокси): http://localhost (направляет на WordPress)

### Настройка WordPress

После запуска откройте http://localhost:8888 и завершите установку WordPress (мастер настройки базы данных должен пройти автоматически, так как переменные окружения уже заданы).

### Использование API

FastAPI доступен по пути `/api`. Примеры эндпоинтов:

- `GET /api/users` — список пользователей
- `GET /api/users/{id}` — информация о пользователе
- `POST /api/users` — создание пользователя

Документация Swagger доступна по адресу http://localhost:8000/docs.

## Конфигурация

### Переменные окружения (.env)

Файл `.env` не обязателен — все переменные имеют значения по умолчанию. Однако для кастомизации рекомендуется создать `.env` из `.env.example`:

```
user=user
pswd=1234
dbname=wordpress
DOMAIN=localhost
HOST=localhost
```

- `user`, `pswd` — учётные данные PostgreSQL (также используются WordPress и FastAPI).
- `dbname` — имя базы данных (по умолчанию `wordpress`).
- `DOMAIN`, `HOST` — используются в конфигурации Nginx (по умолчанию `localhost`).

### Проксирование Nginx

Nginx выступает обратным прокси для WordPress и FastAPI:
- Запросы к `/` → WordPress (контейнер `wordpress`, порт 80)
- Запросы к `/api/` → FastAPI (контейнер `fastapi`, порт 8000)

WordPress доступен извне по порту `8888` (маппинг `8888:80`), но через Nginx используется внутреннее соединение `http://wordpress`. Конфигурация находится в `nginx/app.conf`.

### Расширение FastAPI

Добавьте новые маршруты в `api/routers/` и подключите их в `api/main.py`.

### Расширение WordPress

Установите плагины и темы через админ‑панель WordPress или поместите их в `wordpress/wp-content/plugins/` и `wordpress/wp-content/themes/`.

## Разработка

### Локальная разработка с hot‑reload

Для FastAPI включён режим `--reload` в Dockerfile. Изменения в коде `api/` автоматически перезагружают сервер.

Для WordPress по умолчанию volume отключён (чтобы избежать конфликтов с правами). Чтобы сохранять изменения тем и плагинов, раскомментируйте строку `volumes:` в `docker-compose.yaml` (секция `wordpress`) и убедитесь, что каталог `wordpress/` существует и имеет правильные права.

### Доступ к базе данных

- Хост: `postgres`
- Порт: `5432`
- База данных: `wordpress` (используется и WordPress, и FastAPI)
- Пользователь/пароль: из `.env` (по умолчанию `user`/`1234`)

### Остановка и очистка

```bash
docker-compose down          # остановить контейнеры
docker-compose down -v       # остановить и удалить тома (данные БД будут потеряны)
```

## Особенности и устранение проблем

### WordPress не подключается к базе данных
- Убедитесь, что контейнер PostgreSQL запущен и прошёл healthcheck (`docker-compose logs postgres`).
- Если база данных `wordpress` не создана, удалите том PostgreSQL (`docker-compose down -v`) и перезапустите.
- Проверьте, что переменные окружения `WORDPRESS_DB_USER`, `WORDPRESS_DB_PASSWORD`, `WORDPRESS_DB_NAME` соответствуют настройкам PostgreSQL.

### Ошибка 502 Bad Gateway в Nginx
- Убедитесь, что WordPress контейнер работает (`docker-compose ps`).
- Проверьте конфигурацию Nginx (`nginx/app.conf`): `proxy_pass` должен быть `http://wordpress`.
- Перезапустите Nginx: `docker-compose restart nginx`.

### FastAPI не запускается (ImportError)
- Убедитесь, что зависимости установлены (контейнер FastAPI пересобран).
- Проверьте, что в `api/Dockerfile` указан правильный `PYTHONPATH` и точка входа `api.main:app`.

### Сохранение данных WordPress
По умолчанию volume для WordPress отключён. Чтобы сохранять темы, плагины и загрузки, раскомментируйте `volumes:` в `docker-compose.yaml` (секция `wordpress`) и убедитесь, что каталог `wordpress/` существует.

## Лицензия

MIT