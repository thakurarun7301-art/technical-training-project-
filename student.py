import tkinter as tk
from tkinter import messagebox, ttk
import heapq

# ------------------- Student -------------------
class Student:
    def __init__(self, sid, name, marks):
        self.id = sid
        self.name = name
        self.marks = marks

# ------------------- QuickSort -------------------
def quicksort(arr):
    arr.sort(key=lambda x: x.marks, reverse=True)

# ------------------- Binary Search -------------------
def binary_search(arr, sid):
    low, high = 0, len(arr)-1
    while low <= high:
        mid = (low+high)//2
        if arr[mid].id == sid:
            return arr[mid]
        elif arr[mid].id < sid:
            low = mid+1
        else:
            high = mid-1
    return None

# ------------------- Heap -------------------
def get_top_n(students, n):
    return heapq.nlargest(n, students, key=lambda x: x.marks)

# ------------------- App -------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Performance Analyzer")
        self.root.geometry("900x550")
        self.root.configure(bg="#0f172a")

        self.students = []
        self.ids = set()

        # Style
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#1e293b",
                        foreground="white",
                        rowheight=30,
                        fieldbackground="#1e293b",
                        font=("Segoe UI", 10))

        style.configure("Treeview.Heading",
                        background="#334155",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))

        # Title
        tk.Label(root, text="🎓 Student Performance Analyzer",
                 font=("Segoe UI", 22, "bold"),
                 bg="#0f172a", fg="#38bdf8").pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root, bg="#0f172a")
        btn_frame.pack()

        self.make_btn(btn_frame, "Add Student", self.open_add, 0, 0)
        self.make_btn(btn_frame, "Sort", self.sort_students, 0, 1)
        self.make_btn(btn_frame, "Search", self.open_search, 0, 2)
        self.make_btn(btn_frame, "Top N", self.open_topn, 1, 0)
        self.make_btn(btn_frame, "Show All", self.display, 1, 1)
        self.make_btn(btn_frame, "Exit", root.quit, 1, 2)

        # Table
        frame = tk.Frame(root, bg="#0f172a")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(frame, columns=("ID","Name","Marks"), show="headings")
        for col in ("ID","Name","Marks"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)

    # ------------------- Button Style -------------------
    def make_btn(self, parent, text, cmd, r, c):
        btn = tk.Button(parent, text=text, command=cmd,
                        bg="#38bdf8", fg="black",
                        font=("Segoe UI", 10, "bold"),
                        width=18, height=2, bd=0)
        btn.grid(row=r, column=c, padx=10, pady=10)

        btn.bind("<Enter>", lambda e: btn.config(bg="#0ea5e9"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#38bdf8"))

    # ------------------- ADD -------------------
    def open_add(self):
        win = self.popup("Add Student")

        id_e = self.input_field(win, "ID")
        name_e = self.input_field(win, "Name")
        marks_e = self.input_field(win, "Marks")

        def submit():
            try:
                sid = int(id_e.get())
                name = name_e.get().strip()
                marks = float(marks_e.get())

                # ✅ Validation
                if sid <= 0:
                    messagebox.showerror("Error", "ID must be positive")
                    return

                if name == "":
                    messagebox.showerror("Error", "Name cannot be empty")
                    return

                if not name.replace(" ", "").isalpha():
                    messagebox.showerror("Error", "Name must contain only letters")
                    return

                if marks < 0 or marks > 100:
                    messagebox.showerror("Error", "Marks must be between 0 and 100")
                    return

                if sid in self.ids:
                    messagebox.showerror("Error", "Duplicate ID")
                    return

                self.students.append(Student(sid, name, marks))
                self.ids.add(sid)

                self.display()
                win.destroy()

            except:
                messagebox.showerror("Error", "Invalid Input (Enter correct values)")

        self.submit_btn(win, submit)

    # ------------------- SEARCH -------------------
    def open_search(self):
        win = self.popup("Search Student")
        id_e = self.input_field(win, "Enter ID")

        def search():
            try:
                sid = int(id_e.get())
                self.students.sort(key=lambda x: x.id)
                res = binary_search(self.students, sid)

                if res:
                    messagebox.showinfo("Found", f"{res.name} | {res.marks}")
                else:
                    messagebox.showerror("Not Found", "No student")
            except:
                messagebox.showerror("Error", "Invalid ID")

        self.submit_btn(win, search)

    # ------------------- TOP N -------------------
    def open_topn(self):
        win = self.popup("Top N Students")
        n_e = self.input_field(win, "Enter N")

        def show():
            try:
                n = int(n_e.get())
                top = get_top_n(self.students, n)

                self.clear()
                for s in top:
                    self.tree.insert("", tk.END, values=(s.id, s.name, s.marks))
            except:
                messagebox.showerror("Error", "Invalid Input")

        self.submit_btn(win, show)

    # ------------------- DISPLAY -------------------
    def display(self):
        self.clear()

        if self.students:
            max_marks = max(s.marks for s in self.students)

        for s in self.students:
            tag = "topper" if self.students and s.marks == max_marks else ""
            self.tree.insert("", tk.END, values=(s.id, s.name, s.marks), tags=(tag,))

        self.tree.tag_configure("topper", background="#14532d")

    def sort_students(self):
        quicksort(self.students)
        self.display()

    def clear(self):
        for r in self.tree.get_children():
            self.tree.delete(r)

    # ------------------- UI HELPERS -------------------
    def popup(self, title):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("300x250")
        win.configure(bg="#1e293b")
        return win

    def input_field(self, parent, text):
        tk.Label(parent, text=text, bg="#1e293b", fg="white").pack(pady=5)
        entry = tk.Entry(parent)
        entry.pack(pady=5)
        return entry

    def submit_btn(self, parent, cmd):
        tk.Button(parent, text="Submit",
                  bg="#22c55e", fg="white",
                  width=15, command=cmd).pack(pady=15)

# ------------------- RUN -------------------
root = tk.Tk()
app = App(root)
root.mainloop()