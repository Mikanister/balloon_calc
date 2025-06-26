import tkinter as tk
from tkinter import ttk, messagebox
import math
from balloon_calculations import air_density_at_height, calc_stress, required_balloon_volume, perform_balloon_calculation

# --- Константи ---
MATERIALS = {
    "HDPE": (950, 20e6),
    "TPU": (1200, 35e6),
    "Mylar": (1400, 100e6),
    "Nylon": (1150, 70e6),
    "PET": (1380, 80e6),
}
GAS_DENSITY = {
    "Гелій": 0.1786,
    "Водень": 0.0899,
    "Гаряче повітря": None
}
T0 = 273.15

def main():
    root = tk.Tk()
    root.title("Калькулятор аеростатів")

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(1, weight=1)

    mode_var = tk.StringVar(value="payload")
    material_var = tk.StringVar(value="TPU")
    gas_var = tk.StringVar(value="Гелій")
    material_density_var = tk.StringVar()
    result_var = tk.StringVar()

    def update_density(*_):
        mat = material_var.get()
        if mat in MATERIALS:
            material_density_var.set(str(MATERIALS[mat][0]))

    def update_fields(*_):
        gas = gas_var.get()
        hot_air = gas == "Гаряче повітря"
        is_payload_mode = mode_var.get() == "payload"
        if hot_air:
            label_ground_temp.grid()
            entry_ground_temp.grid()
            label_t_inside.grid()
            entry_t_inside.grid()
        else:
            label_ground_temp.grid_remove()
            entry_ground_temp.grid_remove()
            label_t_inside.grid_remove()
            entry_t_inside.grid_remove()
        if is_payload_mode:
            label_payload.grid_remove()
            entry_payload.grid_remove()
            label_gas_volume.grid()
            entry_gas_volume.grid()
        else:
            label_gas_volume.grid_remove()
            entry_gas_volume.grid_remove()
            label_payload.grid()
            entry_payload.grid()

    def calculate():
        try:
            # Gather all input values
            thickness = float(entry_thickness.get()) / 1e6
            rho_material = float(entry_density.get())
            gas = gas_var.get()
            h0 = float(entry_start_height.get())
            h = h0 + float(entry_work_height.get())
            ground_temp = float(entry_ground_temp.get()) if gas == "Гаряче повітря" else 15
            mode = mode_var.get()
            # Prepare input dict for calculation
            inputs = {
                'thickness': thickness,
                'rho_material': rho_material,
                'gas': gas,
                'h0': h0,
                'h': h,
                'ground_temp': ground_temp,
                'mode': mode,
                'gas_volume': float(entry_gas_volume.get()),
                'desired_payload': float(entry_payload.get()),
                'T_inside': float(entry_t_inside.get()) if gas == "Гаряче повітря" else None,
                'material': material_var.get()
            }
            result = perform_balloon_calculation(inputs)
            result_var.set(result)
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    # --- Віджети ---
    row = 0
    ttk.Label(frame, text="Режим").grid(row=row, column=0, sticky="w")
    ttk.Radiobutton(frame, text="Обʼєм ➜ навантаження", variable=mode_var, value="payload", command=update_fields).grid(row=row, column=1, sticky="w")
    row += 1
    ttk.Radiobutton(frame, text="Навантаження ➜ обʼєм", variable=mode_var, value="volume", command=update_fields).grid(row=row, column=1, sticky="w")
    row += 1

    label_payload = ttk.Label(frame, text="Корисне навантаження (кг)")
    entry_payload = ttk.Entry(frame)
    entry_payload.insert(0, "3")
    label_payload.grid(row=row, column=0, sticky="w")
    entry_payload.grid(row=row, column=1, sticky="ew")
    row += 1

    label_gas_volume = ttk.Label(frame, text="Обʼєм газу (м³)")
    entry_gas_volume = ttk.Entry(frame)
    entry_gas_volume.insert(0, "10")
    label_gas_volume.grid(row=row, column=0, sticky="w")
    entry_gas_volume.grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Матеріал оболонки").grid(row=row, column=0, sticky="w")
    ttk.Combobox(frame, textvariable=material_var, values=list(MATERIALS.keys()), state="readonly").grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Щільність оболонки (кг/м³)").grid(row=row, column=0, sticky="w")
    entry_density = ttk.Entry(frame, textvariable=material_density_var)
    entry_density.grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Товщина оболонки (мкм)").grid(row=row, column=0, sticky="w")
    entry_thickness = ttk.Entry(frame)
    entry_thickness.insert(0, "35")
    entry_thickness.grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Висота пуску над рівнем моря (м)").grid(row=row, column=0, sticky="w")
    entry_start_height = ttk.Entry(frame)
    entry_start_height.insert(0, "0")
    entry_start_height.grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Висота польоту відносно пуску (м)").grid(row=row, column=0, sticky="w")
    entry_work_height = ttk.Entry(frame)
    entry_work_height.insert(0, "1000")
    entry_work_height.grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Label(frame, text="Газ").grid(row=row, column=0, sticky="w")
    ttk.Combobox(frame, textvariable=gas_var, values=list(GAS_DENSITY.keys()), state="readonly").grid(row=row, column=1, sticky="ew")
    row += 1

    label_ground_temp = ttk.Label(frame, text="T на землі (°C)")
    entry_ground_temp = ttk.Entry(frame)
    entry_ground_temp.insert(0, "15")
    label_ground_temp.grid(row=row, column=0, sticky="w")
    entry_ground_temp.grid(row=row, column=1, sticky="ew")
    row += 1

    label_t_inside = ttk.Label(frame, text="T всередині (°C)")
    entry_t_inside = ttk.Entry(frame)
    entry_t_inside.insert(0, "100")
    label_t_inside.grid(row=row, column=0, sticky="w")
    entry_t_inside.grid(row=row, column=1, sticky="ew")
    row += 1

    ttk.Button(frame, text="Обрахувати", command=calculate).grid(row=row, column=0, columnspan=2, pady=10)
    row += 1
    ttk.Label(frame, textvariable=result_var, justify="left", font=("Courier New", 10)).grid(row=row, column=0, columnspan=2, sticky="w")

    # --- Ініціалізація ---
    material_var.trace_add("write", update_density)
    gas_var.trace_add("write", update_fields)
    mode_var.trace_add("write", update_fields)
    update_density()
    update_fields()

    root.mainloop()

if __name__ == "__main__":
    main()
