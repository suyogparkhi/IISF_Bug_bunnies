import tkinter as tk
from tkinter import filedialog
from filecmp import dircmp
import os

class FileCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Compare Tool")

        self.source_label = tk.Label(root, text="Source Directory:")
        self.source_label.pack()

        self.source_entry = tk.Entry(root, width=50)
        self.source_entry.pack()

        self.source_browse_button = tk.Button(root, text="Browse", command=self.browse_source)
        self.source_browse_button.pack()

        self.destination_label = tk.Label(root, text="Destination Directory:")
        self.destination_label.pack()

        self.destination_entry = tk.Entry(root, width=50)
        self.destination_entry.pack()

        self.destination_browse_button = tk.Button(root, text="Browse", command=self.browse_destination)
        self.destination_browse_button.pack()

        self.compare_button = tk.Button(root, text="Compare", command=self.compare_folders)
        self.compare_button.pack()

    def browse_source(self):
        source_dir = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, source_dir)

    def browse_destination(self):
        dest_dir = filedialog.askdirectory()
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, dest_dir)

    def compare_folders(self):
        source_dir = self.source_entry.get()
        dest_dir = self.destination_entry.get()

        if not source_dir or not dest_dir:
            tk.messagebox.showerror("Error", "Both source and destination directories are required.")
            return

        duplicates = self.find_duplicates(source_dir, dest_dir)

        if duplicates:
            tk.messagebox.showinfo("Results", "Duplicate files found:\n{}".format('\n'.join(duplicates)))
        else:
            tk.messagebox.showinfo("Results", "No duplicate files found.")

    def find_duplicates(self, source_dir, dest_dir):
        source_files = self.get_all_files(source_dir)
        dest_files = self.get_all_files(dest_dir)

        duplicate_files = set(source_files) & set(dest_files)
        return list(duplicate_files)

    def get_all_files(self, directory):
        all_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        return all_files

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCompareApp(root)
    root.mainloop()
