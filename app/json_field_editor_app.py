import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from PIL import Image, ImageTk
import pandas as pd
import shutil
import os

# --- Functions ---
def log_message(log_widget, message, msg_type="info"):
    if msg_type == "success":
        log_widget.insert(tk.END, message + "\n", "success")
    elif msg_type == "error":
        log_widget.insert(tk.END, message + "\n", "error")
    elif msg_type == "field":
        log_widget.insert(tk.END, message + "\n", "field")
    else:
        log_widget.insert(tk.END, message + "\n")
    log_widget.see(tk.END)

def get_fields(file_path):
    try:
        df = pd.read_json(file_path)
        return list(df.columns)
    except Exception:
        return []

def update_field_options(*args):
    file_path = file_entry.get()
    fields = get_fields(file_path)
    col_combo['values'] = fields
    oldfield_combo['values'] = fields
    newfield_combo.set("")
    newfield_combo['values'] = []
    newfield_combo['state'] = 'normal'

def change_field_value(file_path, column, old_value, new_value, log_widget):
    try:
        df = pd.read_json(file_path)
        if column not in df.columns:
            log_message(log_widget, f"Error: Field '{column}' not found in file.", "error")
            return
        backup_path = file_path + ".backup"
        shutil.copy(file_path, backup_path)
        log_message(log_widget, f"Backup created: {backup_path}")
        records_to_change = (df[column] == old_value).sum()
        log_message(log_widget, f"{records_to_change} records need to be changed.")
        log_message(log_widget, f"Field modified: '{column}'", "field")
        if old_value != "":
            log_message(log_widget, f"Old value: '{old_value}'", "field")
        if new_value != "":
            log_message(log_widget, f"New value: '{new_value}'", "field")
        df[column] = df[column].replace(old_value, new_value)
        records_changed = (df[column] == new_value).sum()
        log_message(log_widget, f"{records_changed} records were changed.")
        if records_to_change == records_changed and records_to_change > 0:
            df.to_json(file_path, orient="records", force_ascii=False, indent=2)
            log_message(log_widget, f"Successful change. File overwritten: {file_path}", "success")
        else:
            log_message(log_widget, "Error: The number of changed records does not match the expected or there are no records to change.", "error")
    except Exception as e:
        log_message(log_widget, f"Error: {e}", "error")

def change_field_name(file_path, old_field, new_field, log_widget):
    try:
        df = pd.read_json(file_path)
        if old_field not in df.columns:
            log_message(log_widget, f"Error: Field '{old_field}' not found in file.", "error")
            return
        if new_field in df.columns:
            log_message(log_widget, f"Error: Field '{new_field}' already exists in file.", "error")
            return
        backup_path = file_path + ".backup"
        shutil.copy(file_path, backup_path)
        log_message(log_widget, f"Backup created: {backup_path}")
        log_message(log_widget, f"Field renamed: '{old_field}' → '{new_field}'", "field")
        df = df.rename(columns={old_field: new_field})
        df.to_json(file_path, orient="records", force_ascii=False, indent=2)
        log_message(log_widget, f"Field '{old_field}' renamed to '{new_field}'. File overwritten: {file_path}", "success")
    except Exception as e:
        log_message(log_widget, f"Error: {e}", "error")

# --- GUI ---
root = tk.Tk()
root.title("BeLazy JSON Field Editor")
root.configure(bg="#e3f0ff")

# Main frame
main_frame = tk.Frame(root, bg="#e3f0ff")
main_frame.pack(padx=20, pady=20)

# File selection
file_label = tk.Label(main_frame, text="JSON file:", bg="#e3f0ff", fg="#003366", font=("Arial", 11, "bold"))
file_label.grid(row=0, column=0, sticky="e")
file_entry = tk.Entry(main_frame, width=40, bg="#f0f6ff", fg="#003366", font=("Arial", 10))
file_entry.grid(row=0, column=1)
file_entry.bind("<FocusOut>", update_field_options)
file_entry.bind("<Return>", update_field_options)
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)
        update_field_options()
browse_btn = tk.Button(main_frame, text="Browse", command=browse_file, bg="#b3d1ff", fg="#003366", font=("Arial", 10, "bold"))
browse_btn.grid(row=0, column=2)

# --- Change field value ---
value_frame = tk.LabelFrame(main_frame, text="Change Field Value", bg="#e3f0ff", fg="#003366", font=("Arial", 11, "bold"))
value_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

col_label = tk.Label(value_frame, text="Field name:", bg="#e3f0ff", fg="#003366", font=("Arial", 10))
col_label.grid(row=0, column=0)
col_combo = ttk.Combobox(value_frame, state="readonly")
col_combo.grid(row=0, column=1)

oldval_label = tk.Label(value_frame, text="Old value:", bg="#e3f0ff", fg="#003366", font=("Arial", 10))
oldval_label.grid(row=1, column=0)
oldval_entry = tk.Entry(value_frame, bg="#f0f6ff", fg="#003366", font=("Arial", 10))
oldval_entry.grid(row=1, column=1)

newval_label = tk.Label(value_frame, text="New value:", bg="#e3f0ff", fg="#003366", font=("Arial", 10))
newval_label.grid(row=2, column=0)
newval_entry = tk.Entry(value_frame, bg="#f0f6ff", fg="#003366", font=("Arial", 10))
newval_entry.grid(row=2, column=1)

def run_change_value():
    file_path = file_entry.get()
    column = col_combo.get()
    old_value = oldval_entry.get()
    new_value = newval_entry.get()
    change_field_value(file_path, column, old_value, new_value, log_text)
    update_field_options()  # Actualiza los campos después de cambiar un valor
changeval_btn = tk.Button(value_frame, text="Change Value", command=run_change_value, bg="#b3d1ff", fg="#003366", font=("Arial", 10, "bold"))
changeval_btn.grid(row=3, column=0, columnspan=2, pady=5)

# --- Change field name ---
name_frame = tk.LabelFrame(main_frame, text="Change Field Name", bg="#e3f0ff", fg="#003366", font=("Arial", 11, "bold"))
name_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

oldfield_label = tk.Label(name_frame, text="Old field name:", bg="#e3f0ff", fg="#003366", font=("Arial", 10))
oldfield_label.grid(row=0, column=0)
oldfield_combo = ttk.Combobox(name_frame, state="readonly")
oldfield_combo.grid(row=0, column=1)

newfield_label = tk.Label(name_frame, text="New field name:", bg="#e3f0ff", fg="#003366", font=("Arial", 10))
newfield_label.grid(row=1, column=0)
newfield_combo = ttk.Combobox(name_frame, state="normal")
newfield_combo.grid(row=1, column=1)

def run_change_name():
    file_path = file_entry.get()
    old_field = oldfield_combo.get()
    new_field = newfield_combo.get()
    change_field_name(file_path, old_field, new_field, log_text)
    update_field_options()  # Actualiza los campos después de renombrar
changename_btn = tk.Button(name_frame, text="Change Name", command=run_change_name, bg="#b3d1ff", fg="#003366", font=("Arial", 10, "bold"))
changename_btn.grid(row=2, column=0, columnspan=2, pady=5)

# --- Log area ---
log_text = scrolledtext.ScrolledText(main_frame, width=60, height=12, bg="#f0f6ff", fg="#003366", font=("Arial", 10))
log_text.grid(row=3, column=0, columnspan=3, padx=5, pady=10)
log_text.tag_configure("success", foreground="green")
log_text.tag_configure("error", foreground="red")
log_text.tag_configure("field", foreground="orange")

# --- BeLazy Logo (JPEG) ---
logo_path = os.path.join(os.path.dirname(__file__), "BeLazy logo.jpg")
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((120, 40))
    logo_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(main_frame, image=logo_tk, bg="#e3f0ff")
    logo_label.image = logo_tk
    logo_label.grid(row=4, column=0, columnspan=3, pady=(10,0))
else:
    logo_label = tk.Label(main_frame, text="BeLazy", bg="#e3f0ff", fg="#003366", font=("Arial", 16, "bold"))
    logo_label.grid(row=4, column=0, columnspan=3, pady=(10,0))

root.mainloop()
