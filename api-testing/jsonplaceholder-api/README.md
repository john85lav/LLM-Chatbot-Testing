# JSONPlaceholder API Testing

Комплексное тестирование JSONPlaceholder REST API с документированием найденных дефектов.

## Обзор

Данный проект содержит результаты полного тестирования JSONPlaceholder API согласно техническому заданию:
- Исследовательское тестирование GET эндпоинтов
- Тестирование POST операций создания ресурсов
- Документирование найденных дефектов

## Структура проекта

```
jsonplaceholder-api/
├── README.md                    # Этот файл
├── reports/
│   ├── full-test-report.md     # Полный отчет по всем тестам
│   └── bug-report.md           # Формальный bug report
├── postman/
│   └── JSONPlaceholder-API.postman_collection.json
└── scripts/
    └── api_testing_script.py   # Python автоматизация
```

## Основные результаты

### Найденные дефекты:
- **DEF-001 (Критический):** POST без Content-Type создает некорректную JSON структуру
- **DEF-002:** Фиксированный ID=101 для всех POST запросов
- **DEF-003:** Отсутствие валидации данных

### Покрытие тестирования:
- **13 тестовых сценариев** в Postman с автоматизацией
- **100% покрытие** требований технического задания
- **Автоматизированные скрипты** для воспроизведения

## Быстрый старт

### Postman Collection
1. Импортировать файл: `postman/JSONPlaceholder-API.postman_collection.json`
2. Установить переменную `baseURL`: `https://jsonplaceholder.typicode.com/posts`
3. Запустить Collection Runner для всех тестов

### Python автоматизация
```bash
cd scripts/
python3 api_testing_script.py
```

### Ручное тестирование
```bash
# Основной дефект - без Content-Type
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -d '{"title": "Test"}'

# Корректный запрос
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'
```

## Инструменты

- **Postman v11.62.5** - GUI тестирование и автоматизация
- **curl** - командная строка для быстрых тестов  
- **Python 3.x + requests** - скрипты автоматизации
- **Дата тестирования:** 12.09.2025

## Ссылки на отчеты

- [Полный отчет тестирования](reports/full-test-report.md)
- [Bug Report](reports/bug-report.md)
- [Postman Collection](postman/)
- [Python Scripts](scripts/)
Bug Report
Postman Collection
Python Scripts
