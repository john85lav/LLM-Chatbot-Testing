# API документация для тестирования

## Endpoints

### POST /api/chat
Отправка сообщения в чат-бот

**Request:**
```json
{
  "message": "string",
  "conversation_id": "uuid4", 
  "max_tokens": 1000
}
```

**Response:**
```json
{
  "response": "string",
  "conversation_id": "string", 
  "timestamp": "ISO datetime",
  "model": "string"
}
```

### GET /api/health
Проверка состояния API

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "ISO datetime",
  "environment": "production",
  "model": "string"
}
```

## Коды ошибок

- **200**: Успешный запрос
- **400**: Неверный формат запроса
- **500**: Внутренняя ошибка сервера
- **503**: Сервис недоступен
