import tkinter as tk
from tkinter import ttk, messagebox

# Create the main application window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("600x500")

# List to store transactions
transactions = []

# Labels and Input Fields
tk.Label(root, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Category:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Type:").grid(row=2, column=0, padx=5, pady=5)
tk.Label(root, text="Date:").grid(row=3, column=0, padx=5, pady=5)

amount_entry = tk.Entry(root)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

type_var = tk.StringVar()
type_dropdown = ttk.Combobox(root, textvariable=type_var, values=["Income", "Expense"])
type_dropdown.grid(row=2, column=1, padx=5, pady=5)
type_dropdown.current(0)

date_entry = tk.Entry(root)
date_entry.grid(row=3, column=1, padx=5, pady=5)

# Functions for Transactions
def add_transaction():
    amount = amount_entry.get()
    category = category_entry.get()
    trans_type = type_var.get()
    date = date_entry.get()
    
    if not amount or not category or not date:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount!")
        return
    
    transactions.append((amount, category, trans_type, date))
    update_transaction_list()
    clear_entries()

def clear_entries():
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

def delete_transaction():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No transaction selected!")
        return

    for item in selected_item:
        index = tree.index(item)
        transactions.pop(index)
    
    update_transaction_list()

# Transaction Table
frame = tk.Frame(root)
frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
columns = ("Amount", "Category", "Type", "Date")
tree = ttk.Treeview(frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack()

def update_transaction_list():
    tree.delete(*tree.get_children())
    for trans in transactions:
        tree.insert("", tk.END, values=trans)
    update_summary()

def update_summary():
    income = sum(t[0] for t in transactions if t[2] == "Income")
    expense = sum(t[0] for t in transactions if t[2] == "Expense")
    balance = income - expense
    summary_label.config(text=f"Income: {income} | Expense: {expense} | Balance: {balance}")
    check_budget()

def check_budget():
    total_expense = sum(t[0] for t in transactions if t[2] == "Expense")
    if total_expense > 500:  # Example budget limit
        messagebox.showwarning("Budget Alert", "Expenses exceeded 500!")

def filter_transactions():
    selected_category = filter_var.get()
    tree.delete(*tree.get_children())
    for trans in transactions:
        if trans[1] == selected_category or selected_category == "All":
            tree.insert("", tk.END, values=trans)

def sort_transactions():
    transactions.sort(key=lambda x: x[3])
    update_transaction_list()

# Buttons
add_button = tk.Button(root, text="Add Transaction", command=add_transaction)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

delete_button = tk.Button(root, text="Delete Transaction", command=delete_transaction)
delete_button.grid(row=6, column=0, columnspan=2, pady=5)

summary_label = tk.Label(root, text="Income: 0 | Expense: 0 | Balance: 0", font=("Arial", 12, "bold"))
summary_label.grid(row=7, column=0, columnspan=2, pady=10)

filter_var = tk.StringVar()
filter_dropdown = ttk.Combobox(root, textvariable=filter_var, values=["All", "Food", "Transport", "Rent"])
filter_dropdown.grid(row=8, column=0, padx=5, pady=5)
filter_dropdown.current(0)

filter_button = tk.Button(root, text="Filter", command=filter_transactions)
filter_button.grid(row=8, column=1, padx=5, pady=5)

sort_button = tk.Button(root, text="Sort by Date", command=sort_transactions)
sort_button.grid(row=9, column=0, columnspan=2, pady=5)

# Run Tkinter Event Loop
root.mainloop()
