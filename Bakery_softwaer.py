import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Database setup
conn = sqlite3.connect('bakery.db')
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    check_in_time TEXT,
    FOREIGN KEY(employee_id) REFERENCES employees(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    order_details TEXT NOT NULL,
    order_time TEXT
)
''')

conn.commit()

# Tkinter setup
root = tk.Tk()
root.title("Bakery Management System")

# Functions
def add_employee():
    name = entry_employee_name.get()
    if name:
        c.execute("INSERT INTO employees (name) VALUES (?)", (name,))
        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully")
        entry_employee_name.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter a name")

def check_in():
    employee_id = entry_employee_id.get()
    if employee_id:
        c.execute("SELECT name FROM employees WHERE id=?", (employee_id,))
        if c.fetchone():
            check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO attendance (employee_id, check_in_time) VALUES (?, ?)", (employee_id, check_in_time))
            conn.commit()
            messagebox.showinfo("Success", "Check-in recorded successfully")
            entry_employee_id.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Employee ID not found")
    else:
        messagebox.showerror("Error", "Please enter an employee ID")

def add_order():
    customer_name = entry_customer_name.get()
    order_details = entry_order_details.get()
    if customer_name and order_details:
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO orders (customer_name, order_details, order_time) VALUES (?, ?, ?)", (customer_name, order_details, order_time))
        conn.commit()
        messagebox.showinfo("Success", "Order added successfully")
        entry_customer_name.delete(0, tk.END)
        entry_order_details.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter customer name and order details")

def check_orders():
    top = tk.Toplevel()
    top.title("Orders")

    columns = ('#1', '#2', '#3')
    tree = ttk.Treeview(top, columns=columns, show='headings')
    tree.heading('#1', text='Order ID')
    tree.heading('#2', text='Customer Name')
    tree.heading('#3', text='Order Details')
    
    c.execute("SELECT id, customer_name, order_details FROM orders")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    
    tree.pack(expand=True, fill=tk.BOTH)

def check_employee_details():
    top = tk.Toplevel()
    top.title("Employee Details")

    columns = ('#1', '#2')
    tree = ttk.Treeview(top, columns=columns, show='headings')
    tree.heading('#1', text='Employee ID')
    tree.heading('#2', text='Employee Name')
    
    c.execute("SELECT id, name FROM employees")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    
    tree.pack(expand=True, fill=tk.BOTH)

# Tkinter UI
tk.Label(root, text="Employee Name").grid(row=0, column=0, padx=10, pady=10)
entry_employee_name = tk.Entry(root)
entry_employee_name.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Add Employee", command=add_employee).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Employee ID").grid(row=1, column=0, padx=10, pady=10)
entry_employee_id = tk.Entry(root)
entry_employee_id.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Check In", command=check_in).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Customer Name").grid(row=2, column=0, padx=10, pady=10)
entry_customer_name = tk.Entry(root)
entry_customer_name.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Order Details").grid(row=3, column=0, padx=10, pady=10)
entry_order_details = tk.Entry(root)
entry_order_details.grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Add Order", command=add_order).grid(row=3, column=2, padx=10, pady=10)

tk.Button(root, text="Check Orders", command=check_orders).grid(row=4, column=0, columnspan=3, pady=10)
tk.Button(root, text="Check Employee Details", command=check_employee_details).grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()

# Close the database connection
conn.close()
