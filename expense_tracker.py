import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1000x650")
        
        # Initialize database
        self.initialize_db()
        
        # Create UI
        self.create_ui()
        
        # Load initial data
        self.load_expenses()
    
    def initialize_db(self):
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()
        
        # Create table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()
    
    def create_ui(self):
        # Main frames
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.pack(fill=tk.X)
        
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Add Expense Form
        ttk.Label(self.control_frame, text="Amount ($):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.amount_entry = ttk.Entry(self.control_frame, width=10)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.control_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.category_entry = ttk.Combobox(self.control_frame, values=["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"])
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)
        self.category_entry.set("Food")
        
        ttk.Label(self.control_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5, sticky=tk.E)
        self.date_entry = ttk.Entry(self.control_frame, width=12)
        self.date_entry.grid(row=0, column=5, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        ttk.Label(self.control_frame, text="Description:").grid(row=0, column=6, padx=5, pady=5, sticky=tk.E)
        self.desc_entry = ttk.Entry(self.control_frame, width=25)
        self.desc_entry.grid(row=0, column=7, padx=5, pady=5)
        
        # Buttons
        ttk.Button(self.control_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=8, padx=5)
        ttk.Button(self.control_frame, text="Edit Selected", command=self.edit_expense_dialog).grid(row=0, column=9, padx=5)
        ttk.Button(self.control_frame, text="Delete Selected", command=self.delete_expense).grid(row=0, column=10, padx=5)
        
        # Filter Controls
        ttk.Label(self.control_frame, text="Filter by:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        
        self.filter_category = ttk.Combobox(self.control_frame, values=["All"] + ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"])
        self.filter_category.set("All")
        self.filter_category.grid(row=1, column=1, padx=5, pady=5)
        self.filter_category.bind("<<ComboboxSelected>>", lambda e: self.load_expenses())
        
        ttk.Label(self.control_frame, text="From:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.E)
        self.filter_date_from = ttk.Entry(self.control_frame, width=12)
        self.filter_date_from.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(self.control_frame, text="To:").grid(row=1, column=4, padx=5, pady=5, sticky=tk.E)
        self.filter_date_to = ttk.Entry(self.control_frame, width=12)
        self.filter_date_to.grid(row=1, column=5, padx=5, pady=5)
        
        ttk.Button(self.control_frame, text="Apply Filter", command=self.load_expenses).grid(row=1, column=6, padx=5)
        ttk.Button(self.control_frame, text="Reset Filters", command=self.reset_filters).grid(row=1, column=7, padx=5)
        
        # Treeview for displaying expenses
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Amount", "Category", "Date", "Description"), show="headings")
        
        # Configure columns
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Amount", text="Amount ($)", anchor=tk.W)
        self.tree.heading("Category", text="Category", anchor=tk.W)
        self.tree.heading("Date", text="Date", anchor=tk.W)
        self.tree.heading("Description", text="Description", anchor=tk.W)
        
        self.tree.column("ID", width=50, stretch=tk.NO)
        self.tree.column("Amount", width=100, stretch=tk.NO)
        self.tree.column("Category", width=120, stretch=tk.NO)
        self.tree.column("Date", width=120, stretch=tk.NO)
        self.tree.column("Description", width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_expense_dialog())
    
    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()
        description = self.desc_entry.get()
        
        if not amount or not category or not date:
            messagebox.showerror("Error", "Amount, Category, and Date are required!")
            return
        
        try:
            self.cursor.execute( "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
                (float(amount), category, date, description))
            self.conn.commit()
            
            # Clear form and refresh data
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.load_expenses()
            
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")
    
    def edit_expense_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to edit.")
            return
        
        item = self.tree.item(selected[0])
        expense_id = item['values'][0]
        
        # Fetch expense details from DB
        self.cursor.execute("SELECT * FROM expenses WHERE id=?", (expense_id,))
        expense = self.cursor.fetchone()
        
        # Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Expense")
        edit_window.resizable(False, False)
        
        # Form fields
        ttk.Label(edit_window, text="Amount ($):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        amount_entry = ttk.Entry(edit_window, width=15)
        amount_entry.grid(row=0, column=1, padx=5, pady=5)
        amount_entry.insert(0, expense[1])
        
        ttk.Label(edit_window, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        category_entry = ttk.Combobox(edit_window, values=["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"])
        category_entry.grid(row=1, column=1, padx=5, pady=5)
        category_entry.set(expense[2])
        
        ttk.Label(edit_window, text="Date:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        date_entry = ttk.Entry(edit_window, width=15)
        date_entry.grid(row=2, column=1, padx=5, pady=5)
        date_entry.insert(0, expense[3])
        
        ttk.Label(edit_window, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.NE)
        desc_entry = ttk.Entry(edit_window, width=30)
        desc_entry.grid(row=3, column=1, padx=5, pady=5)
        desc_entry.insert(0, expense[4] if expense[4] else "")
        
        # Save button
        ttk.Button(
            edit_window, 
            text="Save Changes",
            command=lambda: self.save_edited_expense(
                expense_id,
                amount_entry.get(),
                category_entry.get(),
                date_entry.get(),
                desc_entry.get(),
                edit_window
            )
        ).grid(row=4, column=0, columnspan=2, pady=10)
    
    def save_edited_expense(self, expense_id, amount, category, date, description, window):
        if not amount or not category or not date:
            messagebox.showerror("Error", "Amount, Category, and Date are required!")
            return
        
        try:
            self.cursor.execute(
                "UPDATE expenses SET amount=?, category=?, date=?, description=? WHERE id=?",
                (float(amount), category, date, description, expense_id)
            )
            self.conn.commit()
            window.destroy()
            self.load_expenses()
            messagebox.showinfo("Success", "Expense updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update expense: {str(e)}")
    
    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete.")
            return
        
        item = self.tree.item(selected[0])
        expense_id = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this expense?"):
            try:
                self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
                self.conn.commit()
                self.load_expenses()
                messagebox.showinfo("Success", "Expense deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete expense: {str(e)}")
    
    def load_expenses(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filter values
        category = self.filter_category.get()
        date_from = self.filter_date_from.get()
        date_to = self.filter_date_to.get()
        
        # Build query
        query = "SELECT * FROM expenses"
        conditions = []
        params = []
        
        if category != "All":
            conditions.append("category = ?")
            params.append(category)
        
        if date_from:
            conditions.append("date >= ?")
            params.append(date_from)
        
        if date_to:
            conditions.append("date <= ?")
            params.append(date_to)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY date DESC"
        
        # Execute query
        self.cursor.execute(query, params)
        expenses = self.cursor.fetchall()
        
        # Insert into treeview
        for expense in expenses:
            self.tree.insert("", tk.END, values=expense)
    
    def reset_filters(self):
        self.filter_category.set("All")
        self.filter_date_from.delete(0, tk.END)
        self.filter_date_to.delete(0, tk.END)
        self.load_expenses()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()