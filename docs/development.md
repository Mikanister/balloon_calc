# Розробка

## Структура проекту

```
balloon/
├── __init__.py
├── main_improved.py      # Точка входу
├── calculations.py       # Основні розрахунки
├── validators.py         # Валідація даних
├── constants.py          # Константи
├── labels.py            # Тексти для GUI
├── models.py            # Pydantic моделі
├── settings.py          # Налаштування
├── export.py            # Експорт даних
├── utils.py             # Утиліти (Rich)
├── gui/                 # GUI модулі
│   ├── widgets.py
│   ├── dialogs.py
│   ├── plotly_3d.py
│   └── ...
├── shapes/              # Геометрія форм
│   ├── sphere.py
│   ├── pillow.py
│   └── ...
├── patterns/            # Викрійки
│   ├── sphere_pattern.py
│   └── ...
└── analysis/            # Аналіз та оптимізація
    ├── optimal_height.py
    └── ...
```

## Запуск тестів

```bash
pytest
pytest --cov=balloon --cov-report=html
```

## Збірка документації

```bash
mkdocs build
mkdocs serve  # Для локального перегляду
```

## Збірка exe

```bash
pyinstaller main_improved.spec
```

## Додавання нових форм

1. Створіть модуль в `balloon/shapes/`
2. Додайте функції: `*_volume`, `*_surface_area`, `*_dimensions_from_volume`
3. Експортуйте в `balloon/shapes/__init__.py`
4. Додайте викрійку в `balloon/patterns/`
5. Оновіть `balloon/labels.py` та `balloon/constants.py`

