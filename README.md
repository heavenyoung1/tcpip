[![CI Pipeline](https://github.com/heavenyoung1/auth_service/actions/workflows/ci.yml/badge.svg)](https://github.com/heavenyoung1/auth_service/actions/workflows/ci.yml)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/heavenyoung1/auth_service/graph/badge.svg?token=19KCUAWC2O)](https://codecov.io/gh/heavenyoung1/auth_service)

# Auth Service - Сервис аутентификации

Данный сервис представляет собой *RESTful API* для управления аутентификацией и авторизацией пользователей. Основная цель — предоставить безопасный механизм регистрации, входа, обновления сессий и выхода из системы с использованием *JSON Web Tokens (JWT)*.

## Оглавление
- [Особенности](#особенности)
- [Технологический стек](#технологический-стек)
- [Концепции аутентификации и авторизации](#концепции-аутентификации-и-авторизации)
  - [Что такое Access Token и Refresh Token и зачем они нужны?](#что-такое-access-token-и-refresh-token-и-зачем-они-нужны)
  - [Взаимодействие Access Token и Refresh Token](#взаимодействие-access-token-и-refresh-token)
- [Быстрый старт](#быстрый-старт)
- [Ручная сборка проекта на OC Linux Ubuntu](#ручная-сборка-проекта-на-oc-linux-ubuntu)
  - [Обновление системы](#обновление-системы)
  - [Установка Python с необходимыми пакетами](#установка-python-с-необходимыми-пакетами)
  - [Установка curl, необходимого для менеджера пакетов uv](#установка-curl-необходимого-для-менеджера-пакетов-uv)
  - [Установка UV - менеджера управления зависимостями](#установка-uv---менеджера-управления-зависимостями)
  - [Клонирование репозитория](#клонирование-репозитория)
  - [Создание виртуального окружения при помощи UV и его активация](#создание-виртуального-окружения-при-помощи-uv-и-его-активация)
  - [Установка зависимостей из файла pyproject.toml](#установка-зависимостей-из-файла-pyproject.toml)
  - [Настройка файла окружения (.env)](#настройка-файла-окружения-env)
- [Работа с Docker](#работа-с-docker)
  - [Создание Docker сети](#создание-docker-сети)
  - [Настройка и запуск контейнера PostgreSQL](#настройка-и-запуск-контейнера-postgresql)
  - [Настройка и запуск контейнера PgAdmin](#настройка-и-запуск-контейнера-pgadmin)
  - [Проверка создания контейнеров](#проверка-создания-контейнеров)
  - [Запуск скрипта для создания БД](#запуск-скрипта-для-создания-бд)
  - [Запуск тестов](#запуск-тестов)
  - [Запустите Uvicorn с явным указанием хоста](#запуск-uvicorn-с-явным-указанием-хоста)
- [Участие в разработке](#участие-в-разработке)

## Особенности

- **Регистрация пользователей**: Создание новых пользователей с помощью `/API/v0.1/register`.
- **Вход пользователей**: Аутентификация пользователей и получение JWT-токенов с помощью `/API/v0.1/login`.
- **Защищенные маршруты**: Доступ к данным пользователя с помощью `/API/v0.1/me` с использованием JWT.
- **Доступ на основе ролей**: Поддерживает роли `user` и `admin` (с возможностью расширения до `/admin-only`).
- **Тесты**: Полный набор тестов с `pytest`.
- **Поддержка докеров**: Готовность к контейнерному развертыванию.

## Технологический стек

**FastAPI**, **SQLAlchemy**, **PostgreSQL**, **JWT**, **Pytest**

# Концепции аутентификации и авторизации
### Что такое Access Token и Refresh Token и зачем они нужны?
**Access Token (токен доступа)** Краткосрочный токен, используемый для аутентификации запросов к защищённым эндпоинтам.
- Предоставляет доступ к защищённым ресурсам (например, `/me`) на основе валидного токена
- Передаётся в заголовке Authorization: Bearer <token>.

**Refresh Token (токен обновления)** Долгосрочный токен, хранящийся в базе данных, позволяющий обновлять *Access Token* без повторного ввода логина и пароля.
- Используется для получения нового *Access Token*, когда старый истёк.
- *Refresh Token* позволяет продлевать сессию без повторной аутентификации, снижая нагрузку на пользователя, но требует безопасного хранения в базе данных.

### Взаимодействие Access Token и Refresh Token

- Пользователь аутентифицируется через `/login`, получая оба токена.
- *Access Token* используется для доступа к API до истечения срока действия.
- При истечении Access Token пользователь отправляет *Refresh Token* на `/refresh`, получая новые токены.
- Выход через `/logout` удаляет *Refresh Token* из базы, завершая сессию.

# Быстрый старт
**1. Клонируйте репозиторий**
```bash
git clone https://github.com/heavenyoung1/auth_service.git
```

**2. Установите и запустите docker-compose**

Важно! Устанавливать docker-compose через `curl`, из GitHub. Данного пакета нет в *apt*. Команда для установки ниже, актуальная версия на данный момент <ins>2.36.0</ins>
```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.36.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

```

**3. Сборка проекта**
```
docker-compose up --build -d
```
*Примечание!* Для удобства в `docker-compose` добавлен `Portainer`, при помощи которого можно удобно управлять контейнерами, просматривать логи через графический интерфейс. Он стартует при сборке докера и доступен по адресу `https://localhost:9443`.

# Ручная сборка проекта на OC Linux Ubuntu

### Обновление системы
```
sudo apt update && sudo apt upgrade -y
```

### Установка Python с необходимыми пакетами
```
sudo apt install python3 python3-pip python3-venv -y
python3 --version
```

### Установка curl, необходимого для менеджера пакетов uv
```
sudo apt install curl
curl --version
```

### Установка UV - менеджера управления зависимостями
```
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

Перейдите в директорию, куда вы хотите клонировать репозиторий

### Клонирование репозитория
```
git clone https://github.com/heavenyoung1/auth_service.git
```

*Важно!* Переоткройте терминал и продолжите выполнение


### Создание виртуального окружения при помощи UV и его активация
```
uv venv
source .venv/bin/activate
```
### Установка зависимостей из файла pyproject.toml (в том числе и dev зависимостей)
```
uv sync --all-extras
```

### Настройка файла окружения (.env)
Для работы проекта необходимо настроить переменные окружения, которые используются для подключения к базе данных и других конфигураций. Эти переменные хранятся в файле `.env`, который должен быть создан в папке `auth_service/`.
1. Перейдите в директорию проекта:
```
cd auth_service
```
2. Создайте файл `.env`:
```
touch .env
```
3. Откройте файл .env в текстовом редакторе (например, `nano`):
```
nano .env
```
4. Добавьте в файл следующие переменные окружения, заменив значения на ваши данные:
```
!!! Для docker-compose вместо <host> прописать название сервера, в данном случае db

# URL для подключения к основной базе данных
DATABASE_URL="postgresql+psycopg2://<user>:<password>@<host>:<port>/<database_name>"

# URL для подключения к тестовой базе данных
TEST_DATABASE_URL="postgresql+psycopg2://<user>:<password>@<host>:<port>/<test_database_name>"

# Секретный ключ для подписи JWT-токенов
SECRET_KEY=<your-secret-key>

# Параметры подключения к PostgreSQL
PG_HOST="<database-host>"
PG_DB="<database-name>"
PG_PORT="<port>"
PG_USER="<username>"
PG_PASSWORD="<password>"
```
5. Cохраните файл и закройте редактор нажмите `Ctrl + O`, затем `Enter`

### Пример заполнения файла .env

```
# URL для подключения к основной базе данных
DATABASE_URL="postgresql+psycopg2://dbuser:securepass123@192.168.1.100:5432/main_db"

# URL для подключения к тестовой базе данных
TEST_DATABASE_URL="postgresql+psycopg2://dbuser:securepass123@192.168.1.100:5432/test_db"

# Секретный ключ для подписи JWT-токенов
SECRET_KEY=my-super-secret-key-987654321

# Параметры подключения к PostgreSQL
PG_HOST="192.168.1.100"
PG_DB="main_db"
PG_PORT="5432"
PG_USER="dbuser"
PG_PASSWORD="securepass123"
```

## Работа с Docker

### Создание Docker сети
```
docker network create auth-network
```

### Настройка и запуск контейнера PostgreSQL
```
docker run -d \
  --name auth-postgres \
  --network auth-network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=P@ssw0rd \
  -e POSTGRES_DB=auth_db \
  -p 5432:5432 \
  postgres:latest
```

### Настройка и запуск контейнера PgAdmin
```
docker run -d \
  --name pgadmin \
  --network auth-network \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=1234 \
  -p 8080:80 \
  dpage/pgadmin4
```

### Проверка создания контейнеров
```
docker ps
```

### Запуск миграции для создания БД и таблиц в БД при помощи Alembic
```
alembic upgrade head
```

### Запуск тестов
```
pytest tests -v
```

### Запустите Uvicorn с явным указанием хоста 
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
`--host 0.0.0.0` разрешает подключения со всех интерфейсов

`--port 8000` явное указание порта

## Участие в разработке
1. Создайте форк репозитория.
2. Создайте ветку: `git checkout -b feature/новая-фича`.
3. Сделайте коммиты с понятными сообщениями (например, `feat: добавлена новая фича`).
4. Отправьте PR в ветку `dev` с описанием изменений.
5. Убедитесь, что CI проходит успешно.

## Установка новых пакетов при помощи uv
```
uv add requests
```