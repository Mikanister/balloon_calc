#!/usr/bin/env python3
"""
Покращений калькулятор аеростатів
Автор: [Ваше ім'я]
Версія: 2.0

Особливості:
- Модульна архітектура
- Валідація введених даних
- Збереження/завантаження налаштувань
- Покращений інтерфейс
- Детальні результати розрахунків
"""

import sys
import os

# Додаємо поточну директорію до шляху для імпорту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui import BalloonCalculatorGUI
    print("Запуск покращеного калькулятора аеростатів...")
    app = BalloonCalculatorGUI()
    app.run()
except ImportError as e:
    print(f"Помилка імпорту: {e}")
    print("Переконайтеся, що всі файли знаходяться в тій самій директорії")
except Exception as e:
    print(f"Помилка запуску: {e}") 