import os
import shutil
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


# Function to extract EXIF date from image files
def get_exif_date(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error reading EXIF date for {file_path}: {e}")
    return None


# Function to organize files by date
def organize_files(source_dir, target_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                try:
                    # Try to get EXIF date first
                    exif_date = get_exif_date(file_path)

                    # Use EXIF date if available, otherwise use the last modified date
                    if exif_date:
                        date_to_use = exif_date
                    else:
                        modified_time = os.path.getmtime(file_path)
                        date_to_use = datetime.fromtimestamp(modified_time)

                    # Create year and month folders based on the date
                    year = date_to_use.strftime('%Y')
                    month = date_to_use.strftime('%B')

                    year_folder = os.path.join(target_dir, year)
                    month_folder = os.path.join(year_folder, month)

                    if not os.path.exists(month_folder):
                        os.makedirs(month_folder)

                    # Print the name of the target folder
                    #print(f"File '{file}' will be moved to: {month_folder}")

                    # Move the file to the appropriate folder
                    shutil.move(file_path, os.path.join(month_folder, file))
                except Exception as e:
                    print(f"Error organizing file {file_path}: {e}")

# Function to select the source directory
def select_source_directory():
    source_dir = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_dir)
    print(f"Source Directory selected: {source_dir}")  # Print the source directory path

# Function to select the target directory
def select_target_directory():
    target_dir = filedialog.askdirectory()
    target_entry.delete(0, tk.END)
    target_entry.insert(0, target_dir)
    print(f"Target Directory selected: {target_dir}")  # Print the target directory path

# Function to start organizing files
def start_organizing():
    source_dir = source_entry.get()
    target_dir = target_entry.get()
    organize_files(source_dir, target_dir)
    tk.messagebox.showinfo("Success", "Files organized successfully!")


# Tkinter GUI setup
root = tk.Tk()
root.title("File Organizer")

root.geometry("620x450")
root.resizable(False,False)
root.configure(bg='#c7f3ff')

logo =tk.PhotoImage(file="logo.png")
tk.Label(root,image=logo,bg="#c7f3ff").place(x=240,y=0)

heading=tk.Label(root,text="File Organizer",
              font='arial 20 bold',fg="#5e17eb",
              bg="#c7f3ff")
heading.place(x=210,y=145)


# GUI elements for source directory selection
tk.Label(root, text="Source Directory:",bg='#c7f3ff',
         font='arial 11 bold',fg="#5e17eb").place(x=30,y=210)
source_entry = tk.Entry(root, width=40,font='arial 11 bold')
source_entry.place(x=170, y=210)
tk.Button(root, text="Browse",width=7,
            cursor='hand2', bg="#03b9ea",fg='white', bd=0,
            command=select_source_directory, activebackground='#ffbb3d',
            font='arial 11 bold').place(x=515, y=205)

# GUI elements for target directory selection
tk.Label(root, text="Target Directory:",bg='#c7f3ff',
         font='arial 11 bold',fg="#5e17eb").place(x=30,y=270)
target_entry = tk.Entry(root, width=40,font='arial 11 bold')
target_entry.place(x=170, y=270)
tk.Button(root, text="Browse",width=7,
            cursor='hand2', bg="#03b9ea",fg='white', bd=0,
            command=select_target_directory, activebackground='#ffbb3d',
            font='arial 11 bold').place(x=515, y=265)

# Button to start the file organizing process
tk.Button(root, text="Organize",width=10,
            cursor='hand2', bg="#03b9ea",fg='white', bd=0,
            command=start_organizing, activebackground='#ffbb3d',
            font='arial 12 bold').place(x=255, y=330)

# insta page
insta_page=tk.Label(root,text="@pythonagham",bg='#c7f3ff',
              fg='#5e17eb',font='arial 10 bold italic')
insta_page.place(x=255,y=400)

# Start the Tkinter event loop
root.mainloop()
