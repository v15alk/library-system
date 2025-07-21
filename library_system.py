import tkinter as tk
from tkinter import messagebox, font

class LibraryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.config(bg="#6a0dad")  # Purple background

        self.books = []

        # Configure root grid for centering
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Heading Frame (row 1)
        heading_frame = tk.Frame(root, bg="#6a0dad")
        heading_frame.grid(row=1, column=1, pady=(20, 10), sticky="nsew")

        heading_font = font.Font(family="Helvetica", size=24, weight="bold")
        subheading_font = font.Font(family="Helvetica", size=14, slant="italic")

        heading_label = tk.Label(heading_frame, text="Library Management", bg="#6a0dad", fg="white", font=heading_font)
        heading_label.pack()

        subheading_label = tk.Label(heading_frame, text="University of Winchester", bg="#6a0dad", fg="white", font=subheading_font)
        subheading_label.pack()

        # Frame to hold form and listbox (row 2)
        self.main_frame = tk.Frame(root, bg="#6a0dad")
        self.main_frame.grid(row=2, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)

        # Variables for form inputs
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.create_form()
        self.create_listbox()
        self.create_buttons()

    def create_form(self):
        form_frame = tk.Frame(self.main_frame, bg="#6a0dad")
        form_frame.grid(row=0, column=0, pady=10, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Label(form_frame, text="Title", bg="#6a0dad", fg="white").grid(row=0, column=0, sticky="e", padx=(0, 10), pady=5)
        tk.Entry(form_frame, textvariable=self.title_var, width=40).grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(form_frame, text="Author", bg="#6a0dad", fg="white").grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)
        tk.Entry(form_frame, textvariable=self.author_var, width=40).grid(row=1, column=1, sticky="ew", pady=5)

        tk.Label(form_frame, text="Year", bg="#6a0dad", fg="white").grid(row=2, column=0, sticky="e", padx=(0, 10), pady=5)
        tk.Entry(form_frame, textvariable=self.year_var, width=40).grid(row=2, column=1, sticky="ew", pady=5)

        tk.Label(form_frame, text="Search", bg="#6a0dad", fg="white").grid(row=3, column=0, sticky="e", padx=(0, 10), pady=5)
        tk.Entry(form_frame, textvariable=self.search_var, width=40).grid(row=3, column=1, sticky="ew", pady=5)

    def create_listbox(self):
        self.book_list = tk.Listbox(self.main_frame, height=10)
        self.book_list.grid(row=4, column=0, sticky="nsew", pady=10, padx=5)
        self.book_list.bind("<<ListboxSelect>>", self.on_select)

        scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.book_list.yview)
        scrollbar.grid(row=4, column=1, sticky='ns', pady=10)
        self.book_list.config(yscrollcommand=scrollbar.set)

    def create_buttons(self):
        btn_frame = tk.Frame(self.main_frame, bg="#6a0dad")
        btn_frame.grid(row=5, column=0, pady=10, sticky="ew")
        btn_frame.grid_columnconfigure(tuple(range(6)), weight=1)

        tk.Button(btn_frame, text="Add Book", command=self.add_book).grid(row=0, column=0, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Update", command=self.update_book).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Delete", command=self.delete_book).grid(row=0, column=2, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Search", command=self.search_books).grid(row=0, column=3, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Check In/Out", command=self.toggle_check).grid(row=0, column=4, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Show All", command=self.display_books).grid(row=0, column=5, padx=5, sticky="ew")

    # (rest of methods remain unchanged — add_book, update_book, delete_book, etc.)

    def add_book(self):
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        year = self.year_var.get().strip()

        if not title or not author or not year:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        self.books.append({
            "title": title,
            "author": author,
            "year": year,
            "status": "Available"
        })
        self.display_books()
        self.clear_form()

    def update_book(self):
        try:
            index = self.book_list.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "No book selected to update")
            return

        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        year = self.year_var.get().strip()

        if not title or not author or not year:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        self.books[index].update({
            "title": title,
            "author": author,
            "year": year
        })
        self.display_books()

    def delete_book(self):
        try:
            index = self.book_list.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "No book selected to delete")
            return

        del self.books[index]
        self.display_books()
        self.clear_form()

    def search_books(self):
        query = self.search_var.get().strip().lower()
        if not query:
            self.display_books()
            return

        filtered = [b for b in self.books if query in b["title"].lower() or query in b["author"].lower()]
        self.display_books(filtered)

    def toggle_check(self):
        try:
            index = self.book_list.curselection()[0]
        except IndexError:
            messagebox.showerror("Error", "No book selected to check in/out")
            return

        book = self.books[index]
        book["status"] = "Checked Out" if book["status"] == "Available" else "Available"
        self.display_books()

    def on_select(self, event):
        try:
            index = self.book_list.curselection()[0]
        except IndexError:
            return

        book = self.books[index]
        self.title_var.set(book["title"])
        self.author_var.set(book["author"])
        self.year_var.set(book["year"])

    def display_books(self, books_to_show=None):
        self.book_list.delete(0, tk.END)
        for book in books_to_show if books_to_show is not None else self.books:
            display_text = f"{book['title']} by {book['author']} ({book['year']}) - {book['status']}"
            self.book_list.insert(tk.END, display_text)

    def clear_form(self):
        self.title_var.set("")
        self.author_var.set("")
        self.year_var.set("")
        self.search_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    root.minsize(500, 400)
    app = LibraryManager(root)
    root.mainloop()