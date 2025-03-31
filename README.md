# FastAPI REST Tronscan service

## Развёртывание локально
Все команды необходимо выполнять в **корневом каталоге проекта**

1. Установка [Docker](https://www.docker.com/get-started/)
2. Скопировать и настроить переменные окружения в файле .env
    ```bash
     copy .env.example .env
    ```
3. Запуск проекта (доступно по адресу https://0.0.0.0:8000)
    ```bash
    docker compose up -d
    ```
4. Остановка проекта и удаление контейнеров и базы данных
    ```bash
    docker compose down -v
    ```
## Прежде чем запустить проект

### Переменные окружения. Файл .env
Для нормальной работы проекта нужно дополнить .env.

## Документация

Документация Swagger API доступна по адресу: http://localhost:8000/api/docs

## Тестовые данные
Адресс тестового кошелька `TNPeeaaFB7K9cmo4uQpcU32zGK8G1NYqeL` из документации TRON API

    
## Чистота кода и линтинг
Чистота кода обеспечивается использованием `task` (конфигурация команд в `Taskfile.yml`), но даже если он не установлен, то команды следующие:
```bash
ruff format .  # Автоформатирование под PEP8
ruff check .   # Проверка на наличие неисправленных ошибок
isort .        # Исправление порядка и вида импортов
mypy .         # Проверка аннотаций типов
```

Для запуска локально необходимо настроить подключение к PostgreSQL, либо запустить контейнер `database` используя команду:
```bash
docker compose up -d database
```
предварительно установив значение `DATABASE_HOST=localhost`.

Также, если необходим Debug, следует настроить конфигурацию debug-сервера.

Для vscode:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.application.api.app:create_app",
                "--host", "127.0.0.1",
                "--port", "8000",
                "--reload"
            ],
            "jinja": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}/src"
            }

        }
    ]
}
```