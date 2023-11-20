import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

class AttendanceManagementSystem:
    def __init__(self, root):
        root.title("Attendance Management System")
        root.geometry("500x300")

        self.student_name_var = tk.StringVar()

        # Menu Bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=root.destroy)

        # Attendance Menu
        attendance_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Attendance", menu=attendance_menu)
        attendance_menu.add_command(label="Mark Attendance", command=self.mark_attendance)
        attendance_menu.add_command(label="View Attendance Records", command=self.load_attendance_records)
        attendance_menu.add_command(label="Check Attendance Percentage", command=self.check_attendance_percentage)
        attendance_menu.add_command(label="View Overall Attendance Percentage", command=self.view_overall_percentage)

        # Entry for student name
        student_name_entry = ttk.Entry(root, textvariable=self.student_name_var)
        student_name_entry.pack(pady=10)

        # Table Panel
        table_panel = ttk.Frame(root, padding=(10, 0, 10, 10))
        table_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        columns = ("ID", "Student Name", "Attendance Date")
        self.tree = ttk.Treeview(table_panel, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(table_panel, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        # Create SQLite database
        self.connection = sqlite3.connect("attendance.db")
        self.create_table()

        # Load initial data
        self.load_attendance_records()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY,
                student_name TEXT NOT NULL,
                attendance_date DATE NOT NULL
            )
        """)
        self.connection.commit()

    def mark_attendance(self):
        student_name = self.student_name_var.get()

        if not student_name:
            messagebox.showinfo("Info", "Please enter a student name.")
            return

        # Insert attendance record
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO attendance (student_name, attendance_date) VALUES (?, ?)",
                       (student_name, str(date.today())))
        self.connection.commit()

        # Reload attendance records after marking
        self.load_attendance_records()

    def load_attendance_records(self):
        # Clear existing tree data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve attendance records
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM attendance")
        records = cursor.fetchall()

        # Populate tree with attendance records
        for record in records:
            self.tree.insert("", "end", values=record)

    def check_attendance_percentage(self):
        student_name = self.student_name_var.get()

        if not student_name:
            messagebox.showinfo("Info", "Please enter a student name.")
            return

        # Count total days
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance")
        total_days = cursor.fetchone()[0]

        # Count days present for the given student
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_name=?", (student_name,))
        present_days = cursor.fetchone()[0]

        if total_days == 0:
            attendance_percentage = 0.0
        else:
            attendance_percentage = (present_days / total_days) * 100

        messagebox.showinfo("Attendance Percentage", f"{student_name}'s attendance percentage is {attendance_percentage:.2f}%.")

    def view_overall_percentage(self):
        # Count total days
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM attendance")
        total_days = cursor.fetchone()[0]

        # Count total students
        cursor.execute("SELECT COUNT(DISTINCT student_name) FROM attendance")
        total_students = cursor.fetchone()[0]

        if total_students == 0:
            overall_percentage = 0.0
        else:
            overall_percentage = (total_days / (total_students * 180)) * 100

        messagebox.showinfo("Overall Attendance Percentage", f"The overall attendance percentage is {overall_percentage:.2f}%.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceManagementSystem(root)
    root.mainloop()
