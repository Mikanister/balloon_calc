# Balloon Calculator

This project is a calculator for aerostats (balloons), featuring a Tkinter GUI and a separate calculation module for easy testing.

## Structure
- `baloon/main_script.py`: Tkinter GUI for the calculator.
- `baloon/balloon_calculations.py`: All calculation logic, importable and testable.
- `tests/unit/test_balloon_calculations.py`: Pytest-based unit tests for the calculation logic.
- `requirements.txt`: Python dependencies (pytest for testing).

## Running the GUI
```bash
python -m baloon.main_script
```

## Running the Tests
```bash
pip install -r requirements.txt
pytest tests/unit/
``` 