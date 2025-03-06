import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import pandas as pd
from fpdf import FPDF

# File to store books
BOOKS_FILE = "books.csv"

# Function to add a book
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    isbn = isbn_entry.get()

    if title and author and year and isbn:
        tree.insert("", tk.END, values=(title, author, year, isbn))
        save_books()
        clear_entries()
    else:
        messagebox.showwarning("Warning", "All fields are required!")

# Function to delete selected book
def delete_book():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
        save_books()
    else:
        messagebox.showwarning("Warning", "Please select a book to delete!")

# Function to search books
def search_book():
    query = search_entry.get().lower()
    for item in tree.get_children():
        values = tree.item(item, "values")
        if query in [v.lower() for v in values]:
            tree.selection_set(item)
            tree.focus(item)
            return
    messagebox.showinfo("Search", "No matching book found.")

# Function to save books to a CSV file
def save_books():
    books = [tree.item(item, "values") for item in tree.get_children()]
    with open(BOOKS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Author", "Year", "ISBN"])
        writer.writerows(books)

# Function to load books from CSV
def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                tree.insert("", tk.END, values=row)

# Function to export books as a PDF file
def generate_pdf():
    books = [tree.item(item, "values") for item in tree.get_children()]
    if not books:
        messagebox.showwarning("Warning", "No books to generate a PDF!")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Library Books Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for book in books:
        pdf.cell(200, 10, f"Title: {book[0]} | Author: {book[1]} | Year: {book[2]} | ISBN: {book[3]}", ln=True)

    pdf.output("Library_Books_Report.pdf")
    messagebox.showinfo("Success", "PDF report generated successfully!")

# Function to clear entry fields
def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)

# Function to export books to CSV
def export_csv():
    books = [tree.item(item, "values") for item in tree.get_children()]
    if books:
        df = pd.DataFrame(books, columns=["Title", "Author", "Year", "ISBN"])
        df.to_csv("Library_Books_List.csv", index=False)
        messagebox.showinfo("Success", "Books exported to CSV successfully!")
    else:
        messagebox.showwarning("Warning", "No books to export!")

# Creating main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

# Title Label
title_label = tk.Label(root, text="Library Management System", font=("Arial", 18, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Form Frame
form_frame = tk.Frame(root, bg="#f0f0f0")
form_frame.pack(pady=5)

tk.Label(form_frame, text="Title:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Author:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
author_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
author_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Year:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5)
year_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
year_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(form_frame, text="ISBN:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5)
isbn_entry = tk.Entry(form_frame, width=30, font=("Arial", 12))
isbn_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons Frame
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Book", font=("Arial", 12), bg="#4CAF50", fg="white", command=add_book)
add_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(button_frame, text="Delete Book", font=("Arial", 12), bg="#f44336", fg="white", command=delete_book)
delete_button.grid(row=0, column=1, padx=5)

pdf_button = tk.Button(button_frame, text="Generate PDF", font=("Arial", 12), bg="#2196F3", fg="white", command=generate_pdf)
pdf_button.grid(row=0, column=2, padx=5)

csv_button = tk.Button(button_frame, text="Export CSV", font=("Arial", 12), bg="#FF9800", fg="white", command=export_csv)
csv_button.grid(row=0, column=3, padx=5)

# Search Bar
search_frame = tk.Frame(root, bg="#f0f0f0")
search_frame.pack(pady=5)

search_entry = tk.Entry(search_frame, width=30, font=("Arial", 12))
search_entry.grid(row=0, column=0, padx=5)

search_button = tk.Button(search_frame, text="Search", font=("Arial", 12), bg="#9C27B0", fg="white", command=search_book)
search_button.grid(row=0, column=1, padx=5)

# Table for Books
columns = ("Title", "Author", "Year", "ISBN")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")
tree.pack(pady=10)

# Load books when app starts
load_books()

# Run main loop
root.mainloop()
