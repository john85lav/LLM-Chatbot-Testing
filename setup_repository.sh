#!/bin/bash
# Скрипт для создания структуры GitHub репозитория

echo "Создание структуры репозитория LLM Chat-bot Testing..."

# Создание основных директорий
mkdir -p test_data
mkdir -p reports  
mkdir -p reports/screenshots
mkdir -p docs

echo "Создание файлов данных..."

# Создание примера тестовых данных
cat > test_data/fact_check_gemini.csv << 'EOF'
question,expected,tolerance
Какова высота Эйфелевой башни?,324,10
Сколько будет 25 * 17?,425,0
В каком году была построена Эйфелева башня?,1889,5
Что такое REST API?,API для взаимодействия программ,0
Сколько дней в году?,365,1
Какая столица Франции?,Париж,0
Сколько будет 100 + 200?,300,0
В каком году началась Вторая мировая война?,1939,1
Что больше: кит или слон?,кит,0
Сколько континентов на Земле?,7,1
EOF

# Расширенные тестовые данные
cat > test_data/sample_tests.csv << 'EOF'
category,question,expected,tolerance,priority
facts,Сколько планет в Солнечной системе?,8,0,high
math,Квадратный корень из 144?,12,0,high
geography,Самая высокая гора в мире?,Эверест,0,medium
tech,Что означает HTTP?,протокол передачи,0,medium
history,В каком году полетел Гагарин?,1961,1,low
EOF

echo "Создание документации..."

# Методология тестирования
cat > docs/testing_methodology.md << 'EOF'
# Методология тестирования LLM чат-ботов

## Основные принципы

### 1. Категории тестирования
- **Functional Testing**: Проверка основного функционала
- **Accuracy Testing**: Фактическая корректность ответов  
- **Context Testing**: Поддержание контекста диалога
- **Safety Testing**: Обработка неэтичных запросов
- **Performance Testing**: Скорость и стабильность ответов

### 2. Критерии оценки
- **Корректность (1-5)**: Фактическая правильность
- **Релевантность (1-5)**: Соответствие запросу
- **Полнота (1-5)**: Достаточность информации  
- **Ясность (1-5)**: Понятность изложения

### 3. Тестовые сценарии
Каждый сценарий должен включать:
- Четкое описание цели
- Входные данные
- Ожидаемые результаты
- Критерии успеха/неуспеха

## Автоматизация

### Когда автоматизировать:
- Регрессионное тестирование
- Массовая проверка фактов
- Performance мониторинг
- Проверка стабильности API

### Когда тестировать вручную:
- Новые фичи
- Сложные сценарии
- UX тестирование
- Исследовательское тестирование
EOF

# API документация
cat > docs/api_documentation.md << 'EOF'
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
EOF

# .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs and reports
*.log
test_report_*.html
reports/*.html

# API keys and secrets
.env
*.key
config.local.*

# Temporary test data
temp_*
test_output_*
EOF

echo "Структура репозитория создана!"
echo ""
echo "Следующие шаги:"
echo "1. git init"
echo "2. git add ."  
echo "3. git commit -m 'Initial commit: LLM Testing Framework'"
echo "4. Создать репозиторий на GitHub"
echo "5. git remote add origin https://github.com/username/llm-chatbot-testing"
echo "6. git push -u origin main"
echo ""
echo "Файлы для копирования в репозиторий:"
echo "- README.md (из артефакта)"
echo "- manual_testing_report.md (готовый отчёт)"  
echo "- automated_testing.py (скрипт автоматизации)"
echo "- requirements.txt"
