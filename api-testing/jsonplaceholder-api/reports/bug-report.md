# Bug Report: POST /posts некорректно обрабатывает запросы без Content-Type header

## Заголовок
POST /posts преобразует JSON в строковый ключ при отсутствии Content-Type header

## Описание
При отправке POST-запроса к `/posts` без указания заголовка `Content-Type: application/json`, API некорректно парсит JSON-данные, преобразуя весь JSON-объект в строковый ключ с пустым значением. Это нарушает принципы HTTP и REST API, создает некорректную структуру данных и может привести к путанице у разработчиков при интеграции с API.

## Окружение
* **API**: JSONPlaceholder (https://jsonplaceholder.typicode.com)
* **Эндпоинт**: POST /posts
* **Инструмент**: curl 8.7.1
* **ОС**: macOS Sequoia 15.6.1  
* **Дата тестирования**: 12.09.2025

## Шаги воспроизведения
1. Отправить POST-запрос БЕЗ Content-Type header:
```bash
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -d '{"title": "Test Post", "body": "Test content"}'
```
2. Сравнить с запросом С Content-Type header:
```bash
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Post", "body": "Test content"}'
```

## Фактический результат
**Запрос без Content-Type:**
```json
{
  "{\"title\": \"Test Post\", \"body\": \"Test content\"}": "",
  "id": 101
}
```
Status: 201 Created

**Запрос с Content-Type:**
```json
{
  "title": "Test Post",
  "body": "Test content",
  "id": 101
}
```
Status: 201 Created

## Ожидаемый результат
При отсутствии корректного Content-Type header для JSON данных API должен:
- Возвращать статус 415 Unsupported Media Type, или
- Возвращать статус 400 Bad Request с сообщением об ошибке, или
- Корректно определять JSON формат и обрабатывать данные правильно

## Серьезность/Приоритет
**Серьезность:** Высокая  
**Приоритет:** Высокий

**Обоснование:** В production среде такое поведение недопустимо, поскольку нарушает фундаментальные принципы HTTP протокола и REST API. Некорректная обработка Content-Type может привести к серьезным проблемам интеграции, неправильной обработке данных клиентскими приложениями и нарушению безопасности API. Production API должен строго валидировать заголовки и возвращать соответствующие error codes для некорректных запросов.

## Доказательства
**Тестирование проведено:** 12.09.2025 

**Инструменты тестирования:**
- curl - результаты выше
- Postman Collection: `JSONPlaceholder API.postman_collection.json` (13 запросов)

**Воспроизводимость:** Дефект стабильно воспроизводится в обоих инструментах тестирования
