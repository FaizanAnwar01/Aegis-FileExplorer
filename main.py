
# ---------------- main.py ----------------
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, scrolledtext
import file_operations as ops
import os
import sys

# --- Theme handling ---
THEME_FILE = "theme.txt"
default_theme = "darkly"

if os.path.exists(THEME_FILE):
    with open(THEME_FILE, "r") as f:
        current_theme = f.read().strip()
else:
    current_theme = default_theme

# Create window with remembered theme
root = tb.Window(themename=current_theme)
root.title("Python File Manager")
root.geometry("1000x750")

source_path = tb.StringVar()
dest_path = tb.StringVar()
file_ext = tb.StringVar()
search_term = tb.StringVar()

def toggle_theme():
    global current_theme
    new_theme = "flatly" if current_theme == "darkly" else "darkly"
    with open(THEME_FILE, "w") as f:
        f.write(new_theme)
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)

def update_progress(current, total):
    progress['value'] = (current / total) * 100
    root.update_idletasks()

def update_status(text):
    status_label.config(text=f"Status: {text}")
    root.update_idletasks()

def browse_source():
    folder = filedialog.askdirectory()
    if folder:
        source_path.set(folder)

def browse_dest():
    folder = filedialog.askdirectory()
    if folder:
        dest_path.set(folder)

def handle_move():
    confirm = messagebox.askyesno("Confirm Move", "Are you sure you want to move these files?")
    if not confirm:
        return
    try:
        ext = ops.parse_extension(file_ext.get())
        update_status("Moving...")
        ops.move_files_by_extension(
            source_path.get(),
            dest_path.get(),
            ext,
            update_progress,
            update_status
        )
        update_status("Done.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status("Idle")

def handle_delete():
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete these files?")
    if not confirm:
        return
    try:
        ext = ops.parse_extension(file_ext.get())
        update_status("Deleting...")
        ops.delete_files_by_extension(
            source_path.get(),
            ext,
            update_progress,
            update_status
        )
        update_status("Done.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status("Idle")

def handle_list_all():
    try:
        update_status("Listing all files...")
        output_text.delete("1.0", "end")
        files = ops.list_files_recursive(source_path.get())
        if not files:
            output_text.insert("end", "No files found.")
        else:
            for f in files:
                output_text.insert("end", f + "\n")
        update_status("Done.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status("Idle")

def handle_list_by_extension():
    try:
        ext = ops.parse_extension(file_ext.get())
        update_status("Listing by extension...")
        output_text.delete("1.0", "end")
        files = ops.list_files_with_extension(source_path.get(), ext)
        if not files:
            output_text.insert("end", f"No files with extension {ext} found.")
        else:
            for f in files:
                output_text.insert("end", f + "\n")
        update_status("Done.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status("Idle")

def handle_search():
    try:
        pattern = search_term.get().strip()
        output_text.delete("1.0", "end")
        if not pattern:
            output_text.insert("end", "Please enter a search term.")
            return
        update_status("Searching...")
        matches = ops.search_files_by_name(source_path.get(), pattern)
        if not matches:
            output_text.insert("end", "No matching files found.")
        else:
            for f in matches:
                output_text.insert("end", f + "\n")
        update_status("Done.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status("Idle")

def handle_undo():
    message = ops.undo_last_action()
    messagebox.showinfo("Undo", message)
    update_status("Undo complete.")

# ---------------- GUI Layout ----------------

# Theme toggle button
tb.Button(root, text="🌓 Toggle Theme", command=toggle_theme, bootstyle="secondary").pack(pady=10)

layout_frame = tb.Frame(root)
layout_frame.pack(pady=15, fill=X)

# Row 1: Source + Search
row1 = tb.Frame(layout_frame)
row1.pack(fill=X, padx=15, pady=10)

tb.Label(row1, text="Source Folder", width=15).pack(side=LEFT, padx=10)
tb.Entry(row1, textvariable=source_path, width=50).pack(side=LEFT, padx=10)
tb.Button(row1, text="Browse", command=browse_source).pack(side=LEFT, padx=10)

tb.Label(row1, text="Search", width=10).pack(side=LEFT, padx=10)
tb.Entry(row1, textvariable=search_term, width=25).pack(side=LEFT, padx=10)
tb.Button(row1, text="Search", command=handle_search, bootstyle="primary").pack(side=LEFT, padx=10)

# Row 2: Destination + Undo
row2 = tb.Frame(layout_frame)
row2.pack(fill=X, padx=15, pady=10)

tb.Label(row2, text="Destination Folder", width=15).pack(side=LEFT, padx=10)
tb.Entry(row2, textvariable=dest_path, width=50).pack(side=LEFT, padx=10)
tb.Button(row2, text="Browse", command=browse_dest).pack(side=LEFT, padx=10)

tb.Button(row2, text="Undo Last Action", command=handle_undo, bootstyle="warning").pack(side=RIGHT, padx=20)

# Row 3: Extension + Actions
row3 = tb.Frame(layout_frame)
row3.pack(fill=X, padx=15, pady=10)

tb.Label(row3, text="File Extension (.txt)", width=18).pack(side=LEFT, padx=10)
tb.Entry(row3, textvariable=file_ext, width=30).pack(side=LEFT, padx=10)

tb.Button(row3, text="Move Files", bootstyle="success", width=15, command=handle_move).pack(side=LEFT, padx=15)
tb.Button(row3, text="Delete Files", bootstyle="danger", width=15, command=handle_delete).pack(side=LEFT, padx=15)

# Row 4: Listing Buttons
row4 = tb.Frame(layout_frame)
row4.pack(fill=X, padx=15, pady=10)

tb.Button(row4, text="List Files by Extension", width=25, command=handle_list_by_extension).pack(side=LEFT, padx=40)
tb.Button(row4, text="List All Files", width=25, command=handle_list_all).pack(side=LEFT, padx=40)

# Output Section
status_label = tb.Label(root, text="Status: Idle", bootstyle="warning")
status_label.pack(pady=10)

progress = tb.Progressbar(root, length=500)
progress.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, height=20, width=115)
output_text.pack(pady=10)

root.mainloop()
