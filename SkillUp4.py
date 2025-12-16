import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

FILENAME = "orders.csv"
MENU = {
    1: ("Кава", 40),
    2: ("Булочка", 25),
    3: ("Сендвіч", 60)
}

def load_orders():
    orders = []
    if not os.path.exists(FILENAME):
        open(FILENAME, "w").close()
        return orders

    with open(FILENAME, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if len(row) == 4:
                orders.append({
                    "id": int(row[0]),
                    "date": row[1],
                    "items": row[2],
                    "sum": int(row[3])
                })
    return orders


def save_order(order):
    with open(FILENAME, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([order["id"], order["date"], order["items"], order["sum"]])


def show_menu():
    text = "МЕНЮ:\n"
    for num, (name, price) in MENU.items():
        text += f"{num}. {name} — {price} грн\n"
    messagebox.showinfo("Меню", text)


def show_orders():
    orders = load_orders()
    if not orders:
        messagebox.showinfo("Замовлення", "Файл порожній.")
        return

    text = ""
    for o in orders:
        text += f'ID: {o["id"]} | {o["date"]} | {o["items"]} | {o["sum"]} грн\n'

    messagebox.showinfo("Усі замовлення", text)


def show_total():
    orders = load_orders()
    total = sum(o["sum"] for o in orders)
    messagebox.showinfo("Загальна виручка", f"Виручка: {total} грн")


def create_order():
    window = tk.Toplevel(root)
    window.title("Нове замовлення")
    window.geometry("350x400")

    tk.Label(window, text="Дата:").pack()
    date_entry = tk.Entry(window)
    date_entry.pack()

    tk.Label(window, text="Оберіть страви:").pack()

    vars_list = {}
    for num, (name, price) in MENU.items():
        var = tk.IntVar()
        tk.Checkbutton(window, text=f"{num}. {name} — {price} грн", variable=var).pack(anchor="w")
        vars_list[num] = var

    def save():
        date = date_entry.get().strip()
        selected = [num for num, v in vars_list.items() if v.get() == 1]

        if not date:
            messagebox.showerror("Помилка", "Введіть дату!")
            return
        if not selected:
            messagebox.showerror("Помилка", "Оберіть хоча б одну страву!")
            return

        items_names = [MENU[n][0] for n in selected]
        total_sum = sum(MENU[n][1] for n in selected)

        orders = load_orders()
        new_id = orders[-1]["id"] + 1 if orders else 1

        order = {
            "id": new_id,
            "date": date,
            "items": ",".join(items_names),
            "sum": total_sum
        }

        save_order(order)
        messagebox.showinfo("Збережено", f"Замовлення ID={new_id} збережено!\nСума: {total_sum} грн")
        window.destroy()

    tk.Button(window, text="Зберегти", command=save, bg="#6bc46b").pack(pady=10)


root = tk.Tk()
root.title("Буфет — Історія замовлень")
root.geometry("350x350")

tk.Button(root, text="Переглянути меню", command=show_menu, width=30).pack(pady=5)
tk.Button(root, text="Створити нове замовлення", command=create_order, width=30).pack(pady=5)
tk.Button(root, text="Переглянути всі замовлення", command=show_orders, width=30).pack(pady=5)
tk.Button(root, text="Показати загальну виручку", command=show_total, width=30).pack(pady=5)
tk.Button(root, text="Вийти", command=root.quit, width=30).pack(pady=5)

root.mainloop()
