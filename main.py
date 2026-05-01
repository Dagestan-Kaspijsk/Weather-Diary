import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД)").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Температура (°C)").grid(row=1, column=0, padx=5, pady=5)
        self.temp_entry = tk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Описание погоды").grid(row=2, column=0, padx=5, pady=5)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Осадки").grid(row=3, column=0, padx=5, pady=5)
        self.precip_var = tk.StringVar(value="нет")
        ttk.Combobox(self.root, textvariable=self.precip_var,
                     values=["да", "нет"], state="readonly").grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить запись", command=self.add_record).grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по дате").grid(row=5, column=0, padx=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=5, column=1, padx=5)
        tk.Button(self.root, text="Фильтровать", command=self.filter_by_date).grid(row=5, column=2, padx=5)

        tk.Label(self.root, text="Фильтр по температуре >").grid(row=6, column=0, padx=5)
        self.filter_temp = tk.Entry(self.root)
        self.filter_temp.grid(row=6, column=1, padx=5)
        tk.Button(self.root, text="Фильтровать", command=self.filter_by_temp).grid(row=6, column=2, padx=5)

        # История записей
        self.columns = ("date", "temp", "desc", "precip")
        self.tree = ttk.Treeview(self.root, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text={"date": "Дата", "temp": "Температура", "desc": "Описание", "precip": "Осадки"}[col])
            self.tree.column(col, width=120)
        self.tree.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.update_tree()

    def validate_input(self):
         date = self.date_entry.get().strip()
         temp = self.temp_entry.get().strip()
         desc = self.desc_entry.get().strip()
         precip = self.precip_var.get()

         if not date or not temp or not desc:
             messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
             return False

         try:
             datetime.strptime(date, "%Y-%m-%d")
         except ValueError:
             messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД.")
             return False

         try:
             float(temp)
         except ValueError:
             messagebox.showerror("Ошибка", "Температура должна быть числом.")
             return False

         return True

    def add_record(self):
         if self.validate_input():
             record = {
                 "date": self.date_entry.get(),
                 "temp": float(self.temp_entry.get()),
                 "desc": self.desc_entry.get(),
                 "precip": self.precip_var.get()
             }
             self.records.append(record)
             self.save_data()
             self.update_tree()
             # Очистка полей
             self.date_entry.delete(0, tk.END)
             self.temp_entry.delete(0, tk.END)
             self.desc_entry.delete(0, tk.END)
             self.precip_var.set("нет")

    def update_tree(self):
         for i in self.tree.get_children():
             self.tree.delete(i)
         for rec in self.records:
             self.tree.insert("", tk.END,
                              values=(rec["date"], rec["temp"], rec["desc"], rec["precip"]))

    def filter_by_date(self):
         date = self.filter_date.get()
         try:
             datetime.strptime(date, "%Y-%m-%d")
         except ValueError:
             messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД.")
             return

         filtered = [r for r in self.records if r["date"] == date]
         self.update_tree_with(filtered)

    def filter_by_temp(self):
         temp = self.filter_temp.get()
         try:
             temp_val = float(temp)
         except ValueError:
             messagebox.showerror("Ошибка", "Температура должна быть числом.")
             return

         filtered = [r for r in self.records if r["temp"] > temp_val]
         self.update_tree_with(filtered)

    def update_tree_with(self, data):
         for i in self.tree.get_children():
             self.tree.delete(i)
         for rec in data:
             self.tree.insert("", tk.END,
                              values=(rec["date"], rec["temp"], rec["desc"], rec["precip"]))

    def save_data(self):
         with open("weather_data.json", "w", encoding="utf-8") as f:
             json.dump(self.records, f, ensure_ascii=False, indent=4)

    def load_data(self):
         if os.path.exists("weather_data.json"):
             with open("weather_data.json", "r", encoding="utf-8") as f:
                 self.records = json.load(f)

if __name__ == "__main__":
     root = tk.Tk()
     app = WeatherDiaryApp(root)
     root.mainloop()