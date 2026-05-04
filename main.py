import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")

        # Поля формы
        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Combobox(root, values=["Кардио", "Силовая", "Йога", "Растяжка"])
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Дата", "Тип", "Длительность"), show="headings")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Длительность", text="Длительность")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(root, values=["Все", "Кардио", "Силовая", "Йога", "Растяжка"])
        self.filter_type.set("Все")
        self.filter_type.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтры", command=self.apply_filters).grid(row=7, column=0, pady=10)
        tk.Button(root, text="Сбросить фильтры", command=self.load_trainings).grid(row=7, column=1, pady=10)

        self.trainings = []
        self.load_trainings()

    def validate_input(self):
        try:
            date = datetime.strptime(self.date_entry.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            return False

        try:
            duration = int(self.duration_entry.get())
            if duration <= 0:
                messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть числом.")
            return False

        if not self.type_entry.get():
            messagebox.showerror("Ошибка", "Укажите тип тренировки.")
            return False

        return True

    def add_training(self):
        if self.validate_input():
            training = {
                "date": self.date_entry.get(),
                "type": self.type_entry.get(),
                "duration": int(self.duration_entry.get())
            }
            self.trainings.append(training)
            self.save_to_json()
            self.load_trainings()
            self.clear_form()

    def apply_filters(self):
        filtered = self.trainings

        # Фильтр по типу
        selected_type = self.filter_type.get()
        if selected_type != "Все":
            filtered = [t for t in filtered if t["type"] == selected_type]

        # Фильтр по дате
        filter_date = self.filter_date.get()
        if filter_date:
            filtered = [t for t in filtered if t["date"] == filter_date]

        self.display_trainings(filtered)

    def save_to_json(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_trainings(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
        except FileNotFoundError:
            self.trainings = []
        self.display_trainings(self.trainings)

    def display_trainings(self, trainings):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for training in trainings:
            self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))

    def clear_form(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.set("")
        self.duration_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
