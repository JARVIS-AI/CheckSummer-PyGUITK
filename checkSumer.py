import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import zlib
from datetime import datetime

def calculate_hash(filepath, algorithms):
    results = {}
    with open(filepath, 'rb') as f:
        file_data = f.read()
        for algo in algorithms:
            if algo == 'MD5':
                results['MD5'] = hashlib.md5(file_data).hexdigest()
            elif algo == 'SHA-1':
                results['SHA-1'] = hashlib.sha1(file_data).hexdigest()
            elif algo == 'SHA-224':
                results['SHA-224'] = hashlib.sha224(file_data).hexdigest()
            elif algo == 'SHA-256':
                results['SHA-256'] = hashlib.sha256(file_data).hexdigest()
            elif algo == 'SHA-384':
                results['SHA-384'] = hashlib.sha384(file_data).hexdigest()
            elif algo == 'SHA-512':
                results['SHA-512'] = hashlib.sha512(file_data).hexdigest()
            elif algo == 'Blake2b':
                results['Blake2b'] = hashlib.blake2b(file_data).hexdigest()
            elif algo == 'CRC32':
                results['CRC32'] = format(zlib.crc32(file_data) & 0xFFFFFFFF, '08x')
    return results

def select_files():
    filepaths = filedialog.askopenfilenames(title="Select Files")
    for filepath in filepaths:
        file_listbox.insert(tk.END, filepath)

def remove_selected_files():
    selected_indices = file_listbox.curselection()
    if selected_indices:
        # Remove the selected files in reverse order to avoid index shifting
        for index in reversed(selected_indices):
            file_listbox.delete(index)
    else:
        messagebox.showwarning("No Selection", "Please select at least one file to remove.")

def generate_checksums():
    selected_algorithms = [algo for algo, var in algorithms.items() if var.get()]
    if not selected_algorithms:
        messagebox.showwarning("No Algorithm", "Please select at least one algorithm.")
        return

    results = {}
    for filepath in file_listbox.get(0, tk.END):
        results[filepath] = calculate_hash(filepath, selected_algorithms)

    display_results(results)

    if save_to_file.get():
        save_results_to_file(results)

def display_results(results):
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    for filepath, hashes in results.items():
        output_text.insert(tk.END, f"\nFile: {filepath}\n")
        for algo, hash_val in hashes.items():
            output_text.insert(tk.END, f"{algo}: {hash_val}\n")
    output_text.config(state=tk.DISABLED)

def save_results_to_file(results):
    with open(f"hash_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
        for filepath, hashes in results.items():
            f.write(f"\nFile: {filepath}\n")
            for algo, hash_val in hashes.items():
                f.write(f"{algo}: {hash_val}\n")

def show_about():
    messagebox.showinfo("About", "Checksum Checker\n\nWritten By JARVIS-AI\nVersion: 1.7.2\nLicense: MIT")

def toggle_validation():
    if validation_option.get() == 1:
        entry_hash.grid(row=5, column=2, columnspan=4, pady=5, padx=10, sticky="we")
        btn_check_file.grid(row=6, column=2, sticky="w", padx=5, pady=10)
        lbl_validation_result.grid(row=6, column=3, columnspan=2, sticky="w")
    else:
        entry_hash.grid_remove()
        btn_check_file.grid_remove()
        lbl_validation_result.grid_remove()

def check_file_validation():
    user_hash = entry_hash.get().strip().lower()
    if not user_hash:
        messagebox.showwarning("Input Error", "Please enter a hash value for validation.")
        return

    selected_algorithms = [algo for algo, var in algorithms.items() if var.get()]
    if not selected_algorithms or file_listbox.size() == 0:
        messagebox.showwarning("Selection Error", "Select at least one file and algorithm to check validation.")
        return

    filepath = file_listbox.get(0)
    calculated_hashes = calculate_hash(filepath, selected_algorithms)
    algorithm = selected_algorithms[0]
    
    if calculated_hashes[algorithm].lower() == user_hash:
        lbl_validation_result.config(text="VALID", fg="green")
    else:
        lbl_validation_result.config(text="INVALID", fg="red")

# GUI Setup
root = tk.Tk()
root.title("Checksum Checker by JARVIS-AI")
root.resizable(False, False)

# Menu
menu_bar = tk.Menu(root)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

# Column 1: Label for file list and Listbox for selected files
tk.Label(root, text="List of Files", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=(10, 0))
file_listbox = tk.Listbox(root, selectmode="multiple", width=40, height=20, font=("Courier", 10))
file_listbox.grid(row=1, column=0, rowspan=6, padx=10, pady=10, ipadx=5, ipady=5)

# Remove Selected Files Button
btn_remove_files = tk.Button(root, text="Remove Selected Files", command=remove_selected_files)
btn_remove_files.grid(row=7, column=0, columnspan=2, pady=10)

# Column 2: Label for results and Text widget for displaying results
tk.Label(root, text="Results", font=("Helvetica", 12, "bold")).grid(row=0, column=1, pady=(10, 0))
output_text = tk.Text(root, wrap="word", width=40, height=20, font=("Courier", 10), state=tk.DISABLED)
output_text.grid(row=1, column=1, rowspan=6, padx=10, pady=10, ipadx=5, ipady=5)

# Column 3: Label for configuration, Checkboxes for algorithms, Save option, and Generate button
tk.Label(root, text="Config", font=("Helvetica", 12, "bold")).grid(row=0, column=2, columnspan=4, pady=(10, 0))

algorithms = {
    "MD5": tk.BooleanVar(),
    "SHA-1": tk.BooleanVar(),
    "SHA-224": tk.BooleanVar(),
    "SHA-256": tk.BooleanVar(),
    "SHA-384": tk.BooleanVar(),
    "SHA-512": tk.BooleanVar(),
    "Blake2b": tk.BooleanVar(),
    "CRC32": tk.BooleanVar()
}

algo_names = list(algorithms.keys())
for i in range(2):
    for j in range(4):
        algo = algo_names[i * 4 + j]
        tk.Checkbutton(root, text=algo, variable=algorithms[algo]).grid(row=i+1, column=2 + j, sticky="w", padx=2)

btn_select_files = tk.Button(root, text="Select Files", command=select_files)
btn_select_files.grid(row=3, column=2, columnspan=2, sticky="w", padx=5)

save_to_file = tk.BooleanVar()
tk.Checkbutton(root, text="Save to Text File", variable=save_to_file).grid(row=3, column=4, columnspan=2, sticky="e", padx=2)

# Validation Option Radio Buttons
validation_option = tk.IntVar(value=2)
tk.Radiobutton(root, text="Check File Validation", variable=validation_option, value=1, command=toggle_validation).grid(row=4, column=2, sticky="w", padx=5, pady=(10, 0))
tk.Radiobutton(root, text="Not Checking Validation", variable=validation_option, value=2, command=toggle_validation).grid(row=4, column=3, sticky="w", padx=5, pady=(10, 0))

# Entry for hash input and Validation button
entry_hash = tk.Entry(root, width=40)
btn_check_file = tk.Button(root, text="Check Validation", command=check_file_validation)
lbl_validation_result = tk.Label(root, text="", font=("Helvetica", 12, "bold"))

# Generate Checksums Button
btn_generate = tk.Button(root, text="Generate Checksums", command=generate_checksums)
btn_generate.grid(row=7, column=2, columnspan=4, pady=10)

root.mainloop()
