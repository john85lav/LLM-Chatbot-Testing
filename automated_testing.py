#!/usr/bin/env python3
"""
Автоматизация тестирования Gemini чат-бота
Требования: pip install requests pandas jinja2
"""

import requests
import pandas as pd
import json
import uuid
import re
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
import argparse

class FastAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def send_message(self, payload: Dict) -> requests.Response:
        """Отправка сообщения в чат-бот"""
        url = f"{self.base_url}/api/chat"
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response

def load_csv(filepath: str) -> List[tuple]:
    """Загрузка тестовых данных из CSV"""
    df = pd.read_csv(filepath)
    return [(row['question'], row['expected'], row['tolerance']) for _, row in df.iterrows()]

def extract_facts(text: str) -> Dict[str, Any]:
    """Извлечение фактов из текста"""
    facts = {}
    
    # Числа
    numbers = re.findall(r'\d+(?:\.\d+)?', text)
    facts['numbers'] = [float(n) for n in numbers]
    
    # Даты
    dates = re.findall(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', text)
    facts['dates'] = dates
    
    # Метры/высота
    height_match = re.search(r'(\d+(?:\.\d+)?)\s*метр', text.lower())
    if height_match:
        facts['height_meters'] = float(height_match.group(1))
    
    # Ключевые слова
    facts['text'] = text.lower()
    
    return facts

def calculate_accuracy(extracted: Dict, expected_facts: Dict, tolerance: float) -> float:
    """Расчет точности с учетом допуска"""
    score = 0.0
    total_checks = 0
    
    # Проверка числовых значений
    if 'height_meters' in expected_facts and 'height_meters' in extracted:
        expected_height = expected_facts['height_meters']
        actual_height = extracted['height_meters']
        diff = abs(expected_height - actual_height)
        if diff <= tolerance:
            score += 1.0
        else:
            score += max(0, 1.0 - (diff / expected_height))
        total_checks += 1
    
    # Проверка наличия ключевых слов
    if 'keywords' in expected_facts:
        for keyword in expected_facts['keywords']:
            if keyword.lower() in extracted['text']:
                score += 1.0
            total_checks += 1
    
    return score / total_checks if total_checks > 0 else 0.0

def log_test_result(result: Dict):
    """Логирование результата теста"""
    timestamp = result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Q: {result['question'][:50]}...")
    print(f"  Expected: {result['expected'][:50]}...")
    print(f"  Actual: {result['actual'][:50]}...")
    print(f"  Accuracy: {result['accuracy']:.2%}")
    print(f"  ID: {result['conversation_id']}")
    print("-" * 80)

def generate_html_report(results: List[Dict], output_file: str = "test_report.html"):
    """Генерация HTML отчета"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gemini Bot Test Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .header { background: #f0f0f0; padding: 15px; border-radius: 5px; }
            .test-result { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
            .accuracy-high { background: #d4edda; }
            .accuracy-medium { background: #fff3cd; }
            .accuracy-low { background: #f8d7da; }
            .summary { background: #e7f3ff; padding: 15px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Gemini Bot Test Report</h1>
            <p><strong>Дата:</strong> {{ timestamp }}</p>
            <p><strong>Всего тестов:</strong> {{ total_tests }}</p>
            <p><strong>Средняя точность:</strong> {{ avg_accuracy }}%</p>
        </div>
        
        <div class="summary">
            <h2>Сводка</h2>
            <ul>
                <li>Высокая точность (>80%): {{ high_accuracy }} тестов</li>
                <li>Средняя точность (50-80%): {{ medium_accuracy }} тестов</li>
                <li>Низкая точность (<50%): {{ low_accuracy }} тестов</li>
            </ul>
        </div>
        
        <h2>Детальные результаты</h2>
        {% for result in results %}
        <div class="test-result {{ result.css_class }}">
            <h3>{{ result.question }}</h3>
            <p><strong>Ожидалось:</strong> {{ result.expected }}</p>
            <p><strong>Получено:</strong> {{ result.actual }}</p>
            <p><strong>Точность:</strong> {{ result.accuracy_percent }}%</p>
            <p><strong>ID разговора:</strong> {{ result.conversation_id }}</p>
            <p><strong>Время:</strong> {{ result.timestamp }}</p>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    
    from jinja2 import Template
    
    # Подготовка данных
    total_tests = len(results)
    avg_accuracy = sum(r['accuracy'] for r in results) / total_tests * 100 if total_tests > 0 else 0
    
    high_accuracy = sum(1 for r in results if r['accuracy'] > 0.8)
    medium_accuracy = sum(1 for r in results if 0.5 <= r['accuracy'] <= 0.8)
    low_accuracy = sum(1 for r in results if r['accuracy'] < 0.5)
    
    # Добавление CSS классов
    for result in results:
        result['accuracy_percent'] = f"{result['accuracy']:.1%}"
        if result['accuracy'] > 0.8:
            result['css_class'] = 'accuracy-high'
        elif result['accuracy'] >= 0.5:
            result['css_class'] = 'accuracy-medium'
        else:
            result['css_class'] = 'accuracy-low'
        result['timestamp'] = result['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    
    template = Template(html_template)
    html_content = template.render(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total_tests=total_tests,
        avg_accuracy=f"{avg_accuracy:.1f}",
        high_accuracy=high_accuracy,
        medium_accuracy=medium_accuracy,
        low_accuracy=low_accuracy,
        results=results
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML отчет сохранен: {output_file}")

def create_sample_csv():
    """Создание примера CSV файла с тестовыми данными"""
    data = {
        'question': [
            'Какова высота Эйфелевой башни?',
            'Сколько будет 25 * 17?',
            'В каком году была построена Эйфелева башня?',
            'Что такое REST API?',
            'Сколько дней в году?'
        ],
        'expected': [
            '324',  # метры
            '425',  # результат умножения
            '1889', # год
            'API для взаимодействия', # ключевые слова
            '365'   # дни
        ],
        'tolerance': [10, 0, 5, 0, 1]  # допустимая погрешность
    }
    
    df = pd.DataFrame(data)
    df.to_csv('fact_check_gemini.csv', index=False, encoding='utf-8')
    print("Создан пример CSV файла: fact_check_gemini.csv")

def automated_fact_checking(api_url: str, csv_file: str):
    """Основная функция автоматизированного тестирования"""
    print("Запуск автоматизированного тестирования...")
    
    # Проверка доступности API
    try:
        client = FastAPIClient(api_url)
        health_response = requests.get(f"{api_url}/api/health")
        health_response.raise_for_status()
        print(f"API доступен: {health_response.json()}")
    except Exception as e:
        print(f"API недоступен: {e}")
        return
    
    # Загрузка тестовых данных
    if not Path(csv_file).exists():
        print(f"CSV файл не найден: {csv_file}")
        print("Создаю пример CSV файла...")
        create_sample_csv()
        csv_file = 'fact_check_gemini.csv'
    
    test_cases = load_csv(csv_file)
    print(f"Загружено {len(test_cases)} тестовых случаев")
    
    results = []
    
    # Выполнение тестов
    for i, (question, expected, tolerance) in enumerate(test_cases, 1):
        print(f"\nТест {i}/{len(test_cases)}: {question[:50]}...")
        
        try:
            # Отправка запроса
            response = client.send_message({
                "message": question,
                "conversation_id": f"test_{uuid.uuid4()}"
            })
            
            response_data = response.json()
            actual_answer = response_data["response"]
            
            # Анализ ответа
            extracted = extract_facts(actual_answer)
            expected_facts = extract_facts(expected)
            
            # Специальная обработка для разных типов вопросов
            if 'метр' in question.lower() or 'высота' in question.lower():
                expected_facts['height_meters'] = float(expected)
            elif any(op in question for op in ['*', '+', '-', '/']):
                expected_facts['numbers'] = [float(expected)]
            elif 'год' in question.lower():
                expected_facts['numbers'] = [float(expected)]
            else:
                expected_facts['keywords'] = expected.split()
            
            accuracy = calculate_accuracy(extracted, expected_facts, float(tolerance))
            
            # Сохранение результата
            result = {
                "question": question,
                "expected": expected,
                "actual": actual_answer,
                "accuracy": accuracy,
                "timestamp": datetime.now(),
                "conversation_id": response_data["conversation_id"]
            }
            
            results.append(result)
            log_test_result(result)
            
        except Exception as e:
            print(f"Ошибка в тесте {i}: {e}")
            results.append({
                "question": question,
                "expected": expected,
                "actual": f"ERROR: {str(e)}",
                "accuracy": 0.0,
                "timestamp": datetime.now(),
                "conversation_id": "error"
            })
    
    # Генерация отчета
    print("\nГенерация отчета...")
    generate_html_report(results)
    
    # Финальная статистика
    if results:
        avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
        print(f"\nСредняя точность: {avg_accuracy:.1%}")
        print(f"Успешных тестов: {sum(1 for r in results if r['accuracy'] > 0.8)}/{len(results)}")

def main():
    parser = argparse.ArgumentParser(description='Автоматизация тестирования Gemini чат-бота')
    parser.add_argument('--api-url', default='http://localhost:8000', help='URL API бота')
    parser.add_argument('--csv-file', default='fact_check_gemini.csv', help='Файл с тестовыми данными')
    parser.add_argument('--create-sample', action='store_true', help='Создать пример CSV файла')
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_csv()
        return
    
    automated_fact_checking(args.api_url, args.csv_file)

if __name__ == "__main__":
    main()
