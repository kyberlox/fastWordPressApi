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
├── wordpress/             # WordPress установка
│   ├── wp-config.php      # Конфигурация WordPress
│   ├── wp-content/        # Темы, плагины, загрузки
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

```
user=user
pswd=1234
dbname=wordpress
DOMAIN=localhost
HOST=localhost
```

### Проксирование Nginx

Nginx настроен так:
- Запросы к `/` → WordPress (порт 8888)
- Запросы к `/api/` → FastAPI (порт 8000)

Конфигурация находится в `nginx/app.conf`.

### Расширение FastAPI

Добавьте новые маршруты в `api/routers/` и подключите их в `api/main.py`.

### Расширение WordPress

Установите плагины и темы через админ‑панель WordPress или поместите их в `wordpress/wp-content/plugins/` и `wordpress/wp-content/themes/`.

## Разработка

### Локальная разработка с hot‑reload

Для FastAPI включён режим `--reload` в Dockerfile. Изменения в коде `api/` автоматически перезагружают сервер.

Для WordPress изменения в `wordpress/` синхронизируются через volume.

### Доступ к базе данных

- Хост: `postgres`
- Порт: `5432`
- База данных: `wordpress` (для WordPress) и `pdb` (для FastAPI, если настроено)
- Пользователь/пароль: из `.env`

### Остановка и очистка

```bash
docker-compose down          # остановить контейнеры
docker-compose down -v       # остановить и удалить тома (данные БД будут потеряны)
```

## Лицензия

MIT