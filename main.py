import json
import os
import random
from tkinter import *
from tkinter import messagebox, ttk

# Файл для сохранения истории
HISTORY_FILE = "tasks.json"

# Предопределённые задачи с категориями
DEFAULT_TASKS = [
    {"title": "Прочитать статью по Python", "category": "учёба"},
    {"title": "Сделать зарядку", "category": "спорт"},
    {"title": "Написать отчёт", "category": "работа"},
    {"title": "Выучить 10 новых слов", "category": "учёба"},
    {"title": "Пробежка 30 минут", "category": "спорт"},
    {"title": "Созвон с командой", "category": "работа"},
    {"title": "Решить задачу на LeetCode", "category": "учёба"},
    {"title": "Отжимания 50 раз", "category": "спорт"},
    {"title": "Проверить почту", "category": "работа"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x550")
        self.root.resizable(False, False)

        # Загрузка истории
        self.history = []
        self.load_history()

        # Переменные
        self.filter_var = StringVar(value="все")

        # Виджеты
        self.create_widgets()
        self.refresh_history_list()

    def create_widgets(self):
        # Верхняя панель: генерация
        top_frame = LabelFrame(self.root, text="Генератор", padx=10, pady=10)
        top_frame.pack(fill=X, padx=10, pady=5)

        self.generate_btn = Button(top_frame, text="Сгенерировать задачу", command=self.generate_task,
                                   bg="#4CAF50", fg="white", font=("Arial", 12), height=2)
        self.generate_btn.pack(fill=X)

        self.current_task_label = Label(top_frame, text="", font=("Arial", 12, "bold"), fg="#333")
        self.current_task_label.pack(pady=10)

        # Добавление новой задачи
        add_frame = LabelFrame(self.root, text="Добавить новую задачу", padx=10, pady=10)
        add_frame.pack(fill=X, padx=10, pady=5)

        Label(add_frame, text="Название:").grid(row=0, column=0, sticky=W)
        self.new_task_entry = Entry(add_frame, width=30)
        self.new_task_entry.grid(row=0, column=1, padx=5)

        Label(add_frame, text="Категория:").grid(row=0, column=2, sticky=W, padx=(10, 0))
        self.new_category_combo = ttk.Combobox(add_frame, values=["учёба", "спорт", "работа"], width=10)
        self.new_category_combo.grid(row=0, column=3, padx=5)
        self.new_category_combo.set("учёба")

        Button(add_frame, text="Добавить", command=self.add_custom_task, bg="#2196F3", fg="white").grid(row=0, column=4, padx=5)

        # Фильтр
        filter_frame = LabelFrame(self.root, text="Фильтр по категории", padx=10, pady=5)
        filter_frame.pack(fill=X, padx=10, pady=5)

        categories = ["все", "учёба", "спорт", "работа"]
        for cat in categories:
            Radiobutton(filter_frame, text=cat.capitalize(), variable=self.filter_var, value=cat,
                        command=self.refresh_history_list).pack(side=LEFT, padx=10)

        # История
        history_frame = LabelFrame(self.root, text="История задач", padx=10, pady=10)
        history_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        scrollbar = Scrollbar(history_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.history_listbox = Listbox(history_frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.history_listbox.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Кнопка очистки истории
        Button(self.root, text="Очистить историю", command=self.clear_history, bg="#f44336", fg="white").pack(pady=5)

    def generate_task(self):
        # Фильтруем доступные задачи по выбранной категории
        if self.filter_var.get() == "все":
            available = self.history + DEFAULT_TASKS
        else:
            cat = self.filter_var.get()
            available = [t for t in (self.history + DEFAULT_TASKS) if t["category"] == cat]

        if not available:
            messagebox.showwarning("Нет задач", f"Нет задач в категории '{self.filter_var.get()}'")
            return

        # Выбираем случайную задачу (можно исключить последнюю, чтобы избежать повторов)
        task = random.choice(available)

        # Добавляем в историю (избегаем дублирования подряд? оставим как есть)
        self.history.append(task)
        self.save_history()
        self.refresh_history_list()

        # Показываем сгенерированную задачу
        self.current_task_label.config(text=f"✅ {task['title']} [{task['category']}]")

    def add_custom_task(self):
        title = self.new_task_entry.get().strip()
        category = self.new_category_combo.get().strip()

        if not title:
            messagebox.showwarning("Ошибка", "Название задачи не может быть пустым!")
            return
        if category not in ["учёба", "спорт", "работа"]:
            messagebox.showwarning("Ошибка", "Выберите категорию из списка!")
            return

        new_task = {"title": title, "category": category}
        self.history.append(new_task)
        self.save_history()
        self.refresh_history_list()
        self.new_task_entry.delete(0, END)
        messagebox.showinfo("Успех", f"Задача '{title}' добавлена в историю!")

    def refresh_history_list(self):
        self.history_listbox.delete(0, END)
        filter_cat = self.filter_var.get()

        for task in self.history:
            if filter_cat == "все" or task["category"] == filter_cat:
                display = f"{task['title']} [{task['category']}]"
                self.history_listbox.insert(END, display)

    def clear_history(self):
        if messagebox.askyesno("Очистка", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.refresh_history_list()
            self.current_task_label.config(text="")

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []
        else:
            self.history = []

if __name__ == "__main__":
    root = Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
