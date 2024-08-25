import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Standardbreite
DEFAULT_WIDTH = 1024

def select_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_paths:
        global images, img_thumbnails, file_paths_list, entry_names
        images = [Image.open(fp) for fp in file_paths]
        file_paths_list = file_paths
        img_thumbnails = []
        entry_names = []  # Liste für die Namenseingabefelder

        # Erstelle Thumbnails und zeige mehrere Bilder gleichzeitig an
        for img in images:
            thumbnail = img.copy()
            thumbnail.thumbnail((256, 256))  # Kleine Vorschaugröße für Multiview
            img_thumbnails.append(ImageTk.PhotoImage(thumbnail))

        display_multiview()

        # Setze die Standardbreite und die Höhe basierend auf dem ersten Bild
        entry_width.delete(0, tk.END)
        entry_height.delete(0, tk.END)
        entry_width.insert(0, DEFAULT_WIDTH)
        if images:
            # Automatische Höhenberechnung basierend auf dem Seitenverhältnis
            height = int(DEFAULT_WIDTH * images[0].height / images[0].width)
            entry_height.insert(0, height)

def display_multiview():
    # Lösche das Canvas und zeige mehrere Bilder gleichzeitig an
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    columns = 4  # Anzahl der Spalten in der Grid-Ansicht
    for idx, img_tk in enumerate(img_thumbnails):
        # Label für Bildvorschau
        lbl = tk.Label(canvas_frame, image=img_tk, bg=canvas_bg_color)
        lbl.grid(row=idx // columns * 2, column=idx % columns, padx=5, pady=5)

        # Namenseingabefelder für jedes Bild
        name_entry = tk.Entry(canvas_frame, bg=entry_bg_color, fg=entry_fg_color)
        base_name = os.path.basename(file_paths_list[idx])
        name_entry.insert(0, os.path.splitext(base_name)[0])  # Setze den Standardnamen
        name_entry.grid(row=idx // columns * 2 + 1, column=idx % columns, padx=5, pady=5)
        entry_names.append(name_entry)

def resize_images():
    if images:
        width = int(entry_width.get())
        height = int(entry_height.get())
        save_dir = filedialog.askdirectory()
        if save_dir:
            for i, img in enumerate(images):
                resized_img = img.resize((width, height))
                
                # Nutze den Namen aus dem jeweiligen Eingabefeld
                new_name = entry_names[i].get() + os.path.splitext(file_paths_list[i])[1]
                save_path = os.path.join(save_dir, new_name)
                resized_img.save(save_path)
                
            messagebox.showinfo("Success", "All images have been resized and saved.")
        else:
            messagebox.showwarning("Warning", "No directory selected.")

# GUI Setup
root = tk.Tk()
root.title("Image Resizer - Multiview with Custom Names")

# Dark Mode Farben
bg_color = "#2E2E2E"
fg_color = "#FFFFFF"
btn_bg_color = "#444444"
btn_fg_color = "#FFFFFF"
entry_bg_color = "#3E3E3E"
entry_fg_color = "#FFFFFF"
canvas_bg_color = "#5E5E5E"

# Setze den Hintergrund der Hauptfläche
root.configure(bg=bg_color)

# Layout
canvas_frame = tk.Frame(root, bg=canvas_bg_color)
canvas_frame.grid(row=0, column=0, columnspan=4)

btn_select = tk.Button(root, text="Select Images", command=select_images, bg=btn_bg_color, fg=btn_fg_color)
btn_select.grid(row=1, column=0, pady=10)

label_width = tk.Label(root, text="Width:", bg=bg_color, fg=fg_color)
label_width.grid(row=2, column=0)

entry_width = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color)
entry_width.grid(row=2, column=1)

label_height = tk.Label(root, text="Height:", bg=bg_color, fg=fg_color)
label_height.grid(row=3, column=0)

entry_height = tk.Entry(root, bg=entry_bg_color, fg=entry_fg_color)
entry_height.grid(row=3, column=1)

btn_resize = tk.Button(root, text="Resize & Save All", command=resize_images, bg=btn_bg_color, fg=btn_fg_color)
btn_resize.grid(row=4, column=0, columnspan=4, pady=10)

root.mainloop()
