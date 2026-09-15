"""Main module providing the GUI interface for the Library System.

Provides view, add, edit, and delete functionality for books.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from database import DatabaseHandler
from Validators import validate_book_data


class LibraryApp(tk.Tk):
    """Primary Tkinter Application Class."""

    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x550")

        # Instantiate database handler
        self.db = DatabaseHandler()

        # Build UI layout
        self.create_widgets()
        self.refresh_book_list()

    def create_widgets(self):
        """Construct GUI components including Treeview and buttons."""

        # --- Table View (Show all books) ---
        table_frame = ttk.Frame(self, padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("isbn", "title", "author", "purchased", "available", "price")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=10
        )

        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("purchased", text="Purchased")
        self.tree.heading("available", text="Available")
        self.tree.heading("price", text="Price ($)")

        self.tree.column("isbn", width=110)
        self.tree.column("title", width=220)
        self.tree.column("author", width=150)
        self.tree.column("purchased", width=80, anchor=tk.CENTER)
        self.tree.column("available", width=80, anchor=tk.CENTER)
        self.tree.column("price", width=80, anchor=tk.E)  # Changed tk.RIGHT to tk.E

        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Action Buttons ---
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill=tk.X)

        add_btn = ttk.Button(
            btn_frame, text="Add Book", command=self.open_add_dialog
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = ttk.Button(
            btn_frame, text="Edit Book", command=self.open_edit_dialog
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ttk.Button(
            btn_frame, text="Remove Book", command=self.delete_book
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(
            btn_frame, text="Refresh", command=self.refresh_book_list
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)

    def refresh_book_list(self):
        """Clear treeview and reload records from database."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        books = self.db.fetch_all_books()
        for book in books:
            # Format price for display
            price = f"{book[5]:.2f}" if book[5] is not None else "N/A"
            formatted_book = (
                book[0],
                book[1],
                book[2],
                book[3],
                book[4],
                price,
            )
            self.tree.insert("", tk.END, values=formatted_book)

    def open_add_dialog(self):
        """Open form dialog to add a new book."""
        BookFormDialog(self, title="Add New Book", on_save=self.save_new_book)

    def save_new_book(self, data, dialog_window):
        """Validate and insert new book into database."""
        is_valid, err_msg = validate_book_data(*data)
        if not is_valid:
            messagebox.showerror("Validation Error", err_msg, parent=dialog_window)
            return

        title, author, isbn, purchased, available, price = data
        price_val = float(price) if price.strip() else None

        try:
            self.db.add_book(
                title,
                author,
                isbn,
                int(purchased),
                int(available),
                price_val,
            )
            messagebox.showinfo("Success", "Book added successfully.")
            dialog_window.destroy()
            self.refresh_book_list()
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"ISBN likely already exists: {e}"
            )

    def open_edit_dialog(self):
        """Open form dialog populated with selected book details."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a book to edit.")
            return

        values = self.tree.item(selected_item[0], "values")
        BookFormDialog(
            self,
            title="Edit Book",
            existing_data=values,
            on_save=self.save_edited_book,
            is_edit=True,
        )

    def save_edited_book(self, data, dialog_window):
        """Validate and save updated book data to database."""
        is_valid, err_msg = validate_book_data(*data)
        if not is_valid:
            messagebox.showerror("Validation Error", err_msg, parent=dialog_window)
            return

        title, author, isbn, purchased, available, price = data
        price_val = float(price) if price.strip() else None

        self.db.update_book(
            title, author, isbn, int(purchased), int(available), price_val
        )
        messagebox.showinfo("Success", "Book updated successfully.")
        dialog_window.destroy()
        self.refresh_book_list()

    def delete_book(self):
        """Delete selected book with required user confirmation."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a book to remove.")
            return

        values = self.tree.item(selected_item[0], "values")
        isbn = values[0]
        title = values[1]

        # Requirement: Confirm deletion before removing
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to remove '{title}' (ISBN: {isbn})?",
        )
        if confirm:
            self.db.delete_book(isbn)
            messagebox.showinfo("Success", "Book removed successfully.")
            self.refresh_book_list()


class BookFormDialog(tk.Toplevel):
    """Popup dialog form for Adding and Editing books."""

    def __init__(
        self, parent, title, on_save, existing_data=None, is_edit=False
    ):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x320")
        self.on_save = on_save
        self.is_edit = is_edit

        self.entries = {}
        fields = [
            ("Title *", "title"),
            ("Author *", "author"),
            ("ISBN *", "isbn"),
            ("Copies Purchased *", "purchased"),
            ("Copies Not Checked Out *", "available"),
            ("Retail Price ($)", "price"),
        ]

        # Layout form fields
        for idx, (label_text, field_key) in enumerate(fields):
            lbl = ttk.Label(self, text=label_text)
            lbl.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)

            entry = ttk.Entry(self, width=30)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[field_key] = entry

        # Populate if editing
        if existing_data:
            self.entries["isbn"].insert(0, existing_data[0])
            self.entries["title"].insert(0, existing_data[1])
            self.entries["author"].insert(0, existing_data[2])
            self.entries["purchased"].insert(0, existing_data[3])
            self.entries["available"].insert(0, existing_data[4])

            price_str = "" if existing_data[5] == "N/A" else existing_data[5]
            self.entries["price"].insert(0, price_str)

            # Prevent primary key (ISBN) modification during edit
            if self.is_edit:
                self.entries["isbn"].config(state="disabled")

        save_btn = ttk.Button(self, text="Save", command=self.submit)
        save_btn.grid(row=len(fields), column=0, columnspan=2, pady=15)

    def submit(self):
        """Extract input data and invoke save callback."""
        # Retrieve value from Entry even if disabled during edit
        isbn_val = (
            self.entries["isbn"].get()
            if not self.is_edit
            else self.entries["isbn"].cget("text") or self.entries["isbn"].get()
        )

        data = (
            self.entries["title"].get(),
            self.entries["author"].get(),
            isbn_val,
            self.entries["purchased"].get(),
            self.entries["available"].get(),
            self.entries["price"].get(),
        )
        self.on_save(data, self)


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()