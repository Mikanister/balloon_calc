"""
Покращений GUI для калькулятора аеростатів
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any
import json
import os
import matplotlib.pyplot as plt
from analysis import calculate_height_profile
import logging

from constants import *
from calculations import calculate_balloon_parameters
from validators import validate_all_inputs, ValidationError
from labels import FIELD_LABELS, FIELD_TOOLTIPS, FIELD_DEFAULTS, COMBOBOX_VALUES, ABOUT_TEXT, BUTTON_LABELS, SECTION_LABELS, PERM_MULT_HINT

logging.basicConfig(
    filename='balloon.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

class BalloonCalculatorGUI:
    """Головний клас GUI для калькулятора аеростатів"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор аеростатів v2.0")
        self.root.geometry("600x700")
        # Встановлюємо темну тему одразу
        try:
            style = ttk.Style()
            style.theme_use('alt')
        except Exception:
            pass
        # Змінні
        self.mode_var = tk.StringVar(value="payload")
        self.material_var = tk.StringVar(value="TPU")
        self.gas_var = tk.StringVar(value="Гелій")
        self.material_density_var = tk.StringVar()
        self.result_var = tk.StringVar()
        # Віджети
        self.entries = {}
        self.labels = {}
        self.setup_ui()
        self.setup_bindings()
        self.load_settings()
        
    def setup_ui(self):
        """Налаштування інтерфейсу"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.create_mode_section(main_frame)
        row = self.create_input_section(main_frame)
        row = self.create_button_section(main_frame, row)
        self.create_result_section(main_frame, row)
        
    def create_mode_section(self, parent):
        """Створення секції вибору режиму"""
        row = 0
        # Заголовок
        ttk.Label(parent, text=SECTION_LABELS['mode'], font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 5)
        )
        row += 1
        # Радіокнопки
        ttk.Radiobutton(
            parent, text="Обʼєм ➜ навантаження",
            variable=self.mode_var, value="payload",
            command=self.update_fields
        ).grid(row=row, column=1, sticky="w")
        row += 1
        ttk.Radiobutton(
            parent, text="Навантаження ➜ обʼєм",
            variable=self.mode_var, value="volume",
            command=self.update_fields
        ).grid(row=row, column=1, sticky="w")
        row += 1
        # Роздільник
        ttk.Separator(parent, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=10
        )
        row += 1
        return row
        
    def create_input_section(self, parent):
        """Створення секції введення даних"""
        row = 4
        # Заголовок
        ttk.Label(parent, text=SECTION_LABELS['params'], font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 5)
        )
        row += 1
        # Поля
        self.labels['payload'] = ttk.Label(parent, text=FIELD_LABELS['payload'])
        self.entries['payload'] = ttk.Entry(parent)
        self.entries['payload'].insert(0, FIELD_DEFAULTS['payload'])
        self.labels['gas_volume'] = ttk.Label(parent, text=FIELD_LABELS['gas_volume'])
        self.entries['gas_volume'] = ttk.Entry(parent)
        self.entries['gas_volume'].insert(0, FIELD_DEFAULTS['gas_volume'])
        ttk.Label(parent, text="Матеріал оболонки").grid(row=row, column=0, sticky="w")
        material_combo = ttk.Combobox(
            parent, textvariable=self.material_var,
            values=list(MATERIALS.keys()), state="readonly"
        )
        material_combo.grid(row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1
        ttk.Label(parent, text=FIELD_LABELS['density']).grid(row=row, column=0, sticky="w")
        self.entries['density'] = ttk.Entry(parent, textvariable=self.material_density_var)
        self.entries['density'].grid(row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1
        ttk.Label(parent, text=FIELD_LABELS['thickness']).grid(row=row, column=0, sticky="w")
        self.entries['thickness'] = ttk.Entry(parent)
        self.entries['thickness'].insert(0, FIELD_DEFAULTS['thickness'])
        self.entries['thickness'].grid(row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1
        ttk.Label(parent, text=FIELD_LABELS['start_height']).grid(row=row, column=0, sticky="w")
        self.entries['start_height'] = ttk.Entry(parent)
        self.entries['start_height'].insert(0, FIELD_DEFAULTS['start_height'])
        self.entries['start_height'].grid(row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1
        ttk.Label(parent, text=FIELD_LABELS['work_height']).grid(row=row, column=0, sticky="w")
        self.entries['work_height'] = ttk.Entry(parent)
        self.entries['work_height'].insert(0, FIELD_DEFAULTS['work_height'])
        self.entries['work_height'].grid(row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1
        ttk.Label(parent, text="Газ").grid(row=row, column=0, sticky="w")
        gas_combo = ttk.Combobox(
            parent, textvariable=self.gas_var,
            values=list(GAS_DENSITY.keys()), state="readonly"
        )
        gas_combo.grid(row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1
        self.labels['ground_temp'] = ttk.Label(parent, text=FIELD_LABELS['ground_temp'])
        self.entries['ground_temp'] = ttk.Entry(parent)
        self.entries['ground_temp'].insert(0, FIELD_DEFAULTS['ground_temp'])
        self.labels['inside_temp'] = ttk.Label(parent, text=FIELD_LABELS['inside_temp'])
        self.entries['inside_temp'] = ttk.Entry(parent)
        self.entries['inside_temp'].insert(0, FIELD_DEFAULTS['inside_temp'])
        self.labels['duration'] = ttk.Label(parent, text=FIELD_LABELS['duration'])
        self.entries['duration'] = ttk.Entry(parent)
        self.entries['duration'].insert(0, FIELD_DEFAULTS['duration'])
        self.labels['duration'].grid(row=row, column=0, sticky="w")
        self.entries['duration'].grid(row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1
        self.labels['perm_mult'] = ttk.Label(parent, text=FIELD_LABELS['perm_mult'])
        self.entries['perm_mult'] = ttk.Combobox(parent, values=COMBOBOX_VALUES['perm_mult'], width=8)
        self.entries['perm_mult'].set(FIELD_DEFAULTS['perm_mult'])
        self.labels['perm_mult'].grid(row=row, column=0, sticky="w")
        self.entries['perm_mult'].grid(row=row, column=1, sticky="ew", padx=(10, 0))
        row += 1
        perm_mult_hint = ttk.Label(parent, text=PERM_MULT_HINT, font=("Arial", 8), foreground="#888")
        perm_mult_hint.grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 20))
        row += 2
        return row
        
    def create_button_section(self, parent, row):
        """Створення секції кнопок"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")
        ttk.Button(
            button_frame, text=BUTTON_LABELS['calculate'],
            command=self.calculate, style="Accent.TButton"
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            button_frame, text=BUTTON_LABELS['show_graph'],
            command=self.show_graph
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            button_frame, text=BUTTON_LABELS['save_settings'],
            command=self.save_settings
        ).pack(side="left", padx=(0, 10))
        ttk.Button(
            button_frame, text=BUTTON_LABELS['clear'],
            command=self.clear_fields
        ).pack(side="left")
        ttk.Button(
            button_frame, text=BUTTON_LABELS['about'],
            command=self.show_about
        ).pack(side="left", padx=(10, 0))
        row += 1
        return row
        
    def create_result_section(self, parent, row):
        """Створення секції результатів"""
        ttk.Label(parent, text=SECTION_LABELS['results'], font=("Arial", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=(0, 5)
        )
        row += 1
        result_label = ttk.Label(
            parent, textvariable=self.result_var,
            justify="left", font=("Courier New", 10),
            background="white", relief="sunken", padding=10
        )
        result_label.grid(row=row, column=0, columnspan=2, sticky="ew", pady=5)
        parent.rowconfigure(row, weight=1)
        
    def setup_bindings(self):
        """Налаштування прив'язок подій"""
        self.add_tooltips()
        self.material_var.trace_add("write", self.update_density)
        self.gas_var.trace_add("write", self.update_fields)
        self.mode_var.trace_add("write", self.update_fields)
        
        # Початкова ініціалізація
        self.update_density()
        self.update_fields()
        
    def update_density(self, *args):
        """Оновлення щільності при зміні матеріалу"""
        mat = self.material_var.get()
        if mat in MATERIALS:
            self.material_density_var.set(str(MATERIALS[mat][0]))
            
    def update_fields(self, *args):
        """Оновлення видимості полів"""
        gas = self.gas_var.get()
        hot_air = gas == "Гаряче повітря"
        is_payload_mode = self.mode_var.get() == "payload"
        
        # Поля для гарячого повітря
        if hot_air:
            self.labels['ground_temp'].grid()
            self.entries['ground_temp'].grid()
            self.labels['inside_temp'].grid()
            self.entries['inside_temp'].grid()
        else:
            self.labels['ground_temp'].grid_remove()
            self.entries['ground_temp'].grid_remove()
            self.labels['inside_temp'].grid_remove()
            self.entries['inside_temp'].grid_remove()
            
        # Поля залежно від режиму
        if is_payload_mode:
            self.labels['payload'].grid_remove()
            self.entries['payload'].grid_remove()
            self.labels['gas_volume'].grid()
            self.entries['gas_volume'].grid()
        else:
            self.labels['gas_volume'].grid_remove()
            self.entries['gas_volume'].grid_remove()
            self.labels['payload'].grid()
            self.entries['payload'].grid()
            
    def calculate(self):
        """Виконання розрахунків"""
        try:
            logging.info("Початок розрахунку. Вхідні дані: %s", {k: v.get() if hasattr(v, 'get') else v for k, v in self.entries.items()})
            # Збір даних з полів
            inputs = {
                'gas_type': self.gas_var.get(),
                'gas_volume': self.entries['gas_volume' if self.mode_var.get() == "payload" else 'payload'].get(),
                'material': self.material_var.get(),
                'thickness': self.entries['thickness'].get(),
                'start_height': self.entries['start_height'].get(),
                'work_height': self.entries['work_height'].get(),
                'ground_temp': self.entries['ground_temp'].get() if self.gas_var.get() == "Гаряче повітря" else "15",
                'inside_temp': self.entries['inside_temp'].get() if self.gas_var.get() == "Гаряче повітря" else "100",
                'duration': self.entries['duration'].get(),
                'mode': self.mode_var.get()
            }
            perm_mult_str = self.entries['perm_mult'].get()
            try:
                perm_mult = float(perm_mult_str)
                if perm_mult <= 0:
                    raise ValueError
            except Exception:
                raise ValidationError("Множник проникності має бути додатним числом")
            # Валідація
            validated_numbers, validated_strings = validate_all_inputs(**inputs)
            # Розрахунки
            results = calculate_balloon_parameters(
                gas_type=validated_strings['gas_type'],
                gas_volume=validated_numbers['gas_volume'],
                material=validated_strings['material'],
                thickness_mm=validated_numbers['thickness'],
                start_height=validated_numbers['start_height'],
                work_height=validated_numbers['work_height'],
                ground_temp=validated_numbers['ground_temp'],
                inside_temp=validated_numbers['inside_temp'],
                duration=validated_numbers['duration'],
                perm_mult=perm_mult,
                mode=validated_strings['mode']
            )
            self.format_results(results, validated_strings['mode'])
            logging.info("Розрахунок успішно завершено.")
        except ValidationError as e:
            logging.warning("Помилка валідації: %s", str(e))
            messagebox.showerror("Помилка валідації", str(e))
        except Exception as e:
            logging.error("Помилка розрахунку: %s", str(e), exc_info=True)
            messagebox.showerror("Помилка розрахунку", str(e))
            
    def format_results(self, results: Dict[str, Any], mode: str):
        """Форматування результатів для відображення"""
        # Встановлюємо ширину для підпису та значення
        label_width = 32
        value_width = 10
        def fmt(label, value, unit=""):
            return f"{label:<{label_width}} {value:>{value_width}} {unit}".rstrip()

        result_lines = []
        if mode == "volume":
            result_lines.append(fmt("Потрібний обʼєм газу:", f"{results['gas_volume']:.2f}", "м³"))
        result_lines.extend([
            fmt("Необхідний обʼєм кулі:", f"{results['required_volume']:.2f}", "м³"),
            fmt("Корисне навантаження (старт):", f"{results['payload']:.2f}", "кг"),
            fmt("Маса оболонки:", f"{results['mass_shell']:.2f}", "кг"),
            fmt("Підйомна сила (старт):", f"{results['lift']:.2f}", "кг"),
            fmt("Радіус кулі:", f"{results['radius']:.2f}", "м"),
            fmt("Площа поверхні:", f"{results['surface_area']:.2f}", "м²"),
            fmt("Щільність повітря:", f"{results['rho_air']:.4f}", "кг/м³"),
            fmt("Підйомна сила на м³:", f"{results['net_lift_per_m3']:.4f}", "кг/м³")
        ])
        # Завжди відображаю втрати газу для гелію/водню
        if self.gas_var.get() in ("Гелій", "Водень"):
            result_lines.append(fmt("Втрати газу за політ:", f"{results['gas_loss']:.6f}", "м³"))
            if results['gas_loss'] < 0.01:
                result_lines.append("Втрати газу дуже малі для цих параметрів (менше 0.01 м³)")
            result_lines.append(fmt("Обʼєм газу в кінці:", f"{results['final_gas_volume']:.2f}", "м³"))
            result_lines.append(fmt("Підйомна сила (кінець):", f"{results['lift_end']:.2f}", "кг"))
            result_lines.append(fmt("Корисне навантаження (кінець):", f"{results['payload_end']:.2f}", "кг"))
            if results['payload_end'] < 0:
                result_lines.append(f"⚠️  Куля втратить підйомну силу до кінця польоту!")
        if self.gas_var.get() == "Гаряче повітря":
            result_lines.extend([
                fmt("T зовні:", f"{results['T_outside_C']:.1f}", "°C"),
                fmt("Макс. напруга:", f"{results['stress'] / 1e6:.2f}", "МПа"),
                fmt("Допустима напруга:", f"{results['stress_limit'] / 1e6:.1f}", "МПа")
            ])
            # Перевірка безпеки
            if results['stress'] > 0:
                safety_factor = results['stress_limit'] / results['stress']
                if safety_factor < 2:
                    result_lines.append(f"⚠️  Коефіцієнт безпеки: {safety_factor:.1f} (низький!)")
                else:
                    result_lines.append(f"✅ Коефіцієнт безпеки: {safety_factor:.1f}")
            else:
                result_lines.append(f"✅ Коефіцієнт безпеки: ∞ (дуже високий, напруга ≈ 0)")
        self.result_var.set('\n'.join(result_lines))
        
    def save_settings(self):
        """Збереження налаштувань"""
        settings = {
            'mode': self.mode_var.get(),
            'material': self.material_var.get(),
            'gas': self.gas_var.get(),
            'thickness': self.entries['thickness'].get(),
            'start_height': self.entries['start_height'].get(),
            'work_height': self.entries['work_height'].get(),
            'ground_temp': self.entries['ground_temp'].get(),
            'inside_temp': self.entries['inside_temp'].get(),
            'payload': self.entries['payload'].get(),
            'gas_volume': self.entries['gas_volume'].get(),
            'perm_mult': self.entries['perm_mult'].get()
        }
        
        try:
            with open('balloon_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            logging.info("Налаштування збережено: %s", settings)
            messagebox.showinfo("Успіх", "Налаштування збережено")
        except Exception as e:
            logging.error("Не вдалося зберегти налаштування: %s", str(e), exc_info=True)
            messagebox.showerror("Помилка", f"Не вдалося зберегти налаштування: {e}")
            
    def load_settings(self):
        """Завантаження налаштувань"""
        try:
            if os.path.exists('balloon_settings.json'):
                with open('balloon_settings.json', 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                logging.info("Завантажено налаштування: %s", settings)
                
                # Встановлення значень
                self.mode_var.set(settings.get('mode', 'payload'))
                self.material_var.set(settings.get('material', 'TPU'))
                self.gas_var.set(settings.get('gas', 'Гелій'))
                
                if 'thickness' in settings:
                    self.entries['thickness'].delete(0, tk.END)
                    self.entries['thickness'].insert(0, settings['thickness'])
                    
                if 'start_height' in settings:
                    self.entries['start_height'].delete(0, tk.END)
                    self.entries['start_height'].insert(0, settings['start_height'])
                    
                if 'work_height' in settings:
                    self.entries['work_height'].delete(0, tk.END)
                    self.entries['work_height'].insert(0, settings['work_height'])
                    
                if 'ground_temp' in settings:
                    self.entries['ground_temp'].delete(0, tk.END)
                    self.entries['ground_temp'].insert(0, settings['ground_temp'])
                    
                if 'inside_temp' in settings:
                    self.entries['inside_temp'].delete(0, tk.END)
                    self.entries['inside_temp'].insert(0, settings['inside_temp'])
                    
                if 'payload' in settings:
                    self.entries['payload'].delete(0, tk.END)
                    self.entries['payload'].insert(0, settings['payload'])
                    
                if 'gas_volume' in settings:
                    self.entries['gas_volume'].delete(0, tk.END)
                    self.entries['gas_volume'].insert(0, settings['gas_volume'])
                    
                if 'perm_mult' in settings:
                    self.entries['perm_mult'].delete(0, tk.END)
                    self.entries['perm_mult'].insert(0, settings['perm_mult'])
                    
        except Exception as e:
            logging.error("Помилка завантаження налаштувань: %s", str(e), exc_info=True)
            print(f"Помилка завантаження налаштувань: {e}")
            
    def clear_fields(self):
        """Очищення всіх полів"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries['thickness'].insert(0, FIELD_DEFAULTS['thickness'])
        self.entries['start_height'].insert(0, FIELD_DEFAULTS['start_height'])
        self.entries['work_height'].insert(0, FIELD_DEFAULTS['work_height'])
        self.entries['ground_temp'].insert(0, FIELD_DEFAULTS['ground_temp'])
        self.entries['inside_temp'].insert(0, FIELD_DEFAULTS['inside_temp'])
        self.entries['payload'].insert(0, FIELD_DEFAULTS['payload'])
        self.entries['gas_volume'].insert(0, FIELD_DEFAULTS['gas_volume'])
        self.entries['perm_mult'].insert(0, FIELD_DEFAULTS['perm_mult'])
        self.result_var.set("")
        
    def run(self):
        """Запуск додатку"""
        self.root.mainloop()

    def show_graph(self):
        """Показати графік залежності параметрів від висоти"""
        try:
            # Збір даних з полів
            inputs = {
                'gas_type': self.gas_var.get(),
                'material': self.material_var.get(),
                'thickness_mm': float(self.entries['thickness'].get()),
                'gas_volume': float(self.entries['gas_volume'].get() if self.mode_var.get() == "payload" else self.entries['payload'].get()),
                'ground_temp': float(self.entries['ground_temp'].get() if self.gas_var.get() == "Гаряче повітря" else 15),
                'inside_temp': float(self.entries['inside_temp'].get() if self.gas_var.get() == "Гаряче повітря" else 100),
                'max_height': 5000
            }
            profile = calculate_height_profile(**inputs)
            heights = [p['height'] for p in profile]
            payloads = [p['payload'] for p in profile]
            lifts = [p['lift'] for p in profile]
            stresses = [p['net_lift_per_m3'] for p in profile]

            plt.figure(figsize=(8, 5))
            plt.plot(heights, payloads, label='Корисне навантаження (кг)')
            plt.plot(heights, lifts, label='Підйомна сила (кг)')
            plt.plot(heights, stresses, label='Підйомна сила на м³ (кг/м³)')
            plt.xlabel('Висота, м')
            plt.ylabel('Значення')
            plt.title('Залежність параметрів аеростата від висоти')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Помилка графіка", str(e))

    def show_about(self):
        """Показати інформацію про програму"""
        messagebox.showinfo(BUTTON_LABELS['about'], ABOUT_TEXT)

    def add_tooltips(self):
        """Додає підказки до всіх полів"""
        for key, entry in self.entries.items():
            if key in FIELD_TOOLTIPS:
                self.create_tooltip(entry, FIELD_TOOLTIPS[key])

    def create_tooltip(self, widget, text):
        """Створює підказку для віджета"""
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1, font=("Arial", 9))
        label.pack(ipadx=1)
        def enter(event):
            x = widget.winfo_rootx() + 20
            y = widget.winfo_rooty() + 20
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()
        def leave(event):
            tooltip.withdraw()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)


if __name__ == "__main__":
    app = BalloonCalculatorGUI()
    app.run() 