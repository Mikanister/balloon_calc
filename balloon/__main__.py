#!/usr/bin/env python3
"""
Entry point для запуску калькулятора аеростатів як модуля:
    python -m balloon
"""

import sys
import os

def main():
    """Головна функція запуску"""
    try:
        # Використовуємо Rich для красивого виводу, якщо доступний
        try:
            from balloon.utils import print_success, print_error
            print_success("Запуск калькулятора аеростатів...")
        except ImportError:
            print("Запуск калькулятора аеростатів...")
        
        # Імпортуємо GUI
        from balloon.gui_main import BalloonCalculatorGUI
        
        app = BalloonCalculatorGUI()
        app.run()
    except Exception as e:
        try:
            from balloon.utils import print_error
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

