#!/usr/bin/env python3
"""
Покращений калькулятор аеростатів
Автор: пан Юрій
Версія: 2.0

Особливості:
- Модульна архітектура
- Валідація введених даних
- Збереження/завантаження налаштувань
- Покращений інтерфейс з темною темою
- Детальні результати розрахунків
- Порівняння матеріалів
- Розрахунок оптимальної висоти
- Розрахунок часу польоту
- Вбудована довідка
- Підтримка неідеальних форм
"""

import sys
import os

def main():
    """Головна функція запуску"""
    # Для PyInstaller exe: PyInstaller сам налаштовує sys.path через spec файл
    # Для звичайного запуску: Python сам знаходить модулі через PYTHONPATH або структуру пакету
    
    try:
        # Використовуємо Rich для красивого виводу, якщо доступний
        try:
            from baloon.utils import print_success, print_error
            print_success("Запуск покращеного калькулятора аеростатів...")
        except ImportError:
            print("Запуск покращеного калькулятора аеростатів...")
        
        # Імпортуємо GUI - Python сам знайде модуль через структуру пакету
        from baloon.gui_main import BalloonCalculatorGUI
        
        app = BalloonCalculatorGUI()
        app.run()
    except ImportError as e:
        # Якщо не вдалося імпортувати, виводимо діагностику
        print(f"Помилка імпорту: {e}")
        print(f"sys.path: {sys.path}")
        print(f"Поточна директорія: {os.getcwd()}")
        if getattr(sys, 'frozen', False):
            print(f"sys._MEIPASS: {sys._MEIPASS}")
        import traceback
        traceback.print_exc()
        if not getattr(sys, 'frozen', False):
            input("Натисніть Enter для виходу...")
        sys.exit(1)
    except Exception as e:
        try:
            from baloon.utils import print_error
            print_error(f"Помилка запуску: {e}")
        except ImportError:
            print(f"Помилка запуску: {e}")
        import traceback
        traceback.print_exc()
        if not getattr(sys, 'frozen', False):
            input("Натисніть Enter для виходу...")
        sys.exit(1)

if __name__ == "__main__":
    main() 