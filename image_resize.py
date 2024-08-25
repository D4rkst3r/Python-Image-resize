import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Standardbreite
DEFAULT_WIDTH = 1024

# Initialisierung der globalen Variablen
images = []
img_thumbnails = []
file_paths_list = []
entry_names = []
resolution_labels = []
canvas_frame = None

def select_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_paths:
        global images, img_thumbnails, file_paths_list, entry_names, resolution_labels, canvas_frame
        images = [Image.open(fp) for fp in file_paths]
        file_paths_list = file_paths
        img_thumbnails = []
        entry_names = []  # Liste für die Namenseingabefelder
        resolution_labels = []  # Liste für die Auflösungsanzeigen

        # Erstelle Thumbnails und zeige mehrere Bilder gleichzeitig an
        for img in images:
            thumbnail = img.copy()
            thumbnail.thumbnail((150, 150))  # Kleine Vorschaugröße für Multiview
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
    global canvas_frame
    # Zerstöre das alte Frame, wenn es existiert
    if canvas_frame:
        canvas_frame.destroy()

    # Erstelle einen neuen Frame im Canvas
    canvas_frame = tk.Frame(canvas, bg=canvas_bg_color)
    canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    # Erstelle Widgets für die Bilder und ihre Eigenschaften
    for idx, img_tk in enumerate(img_thumbnails):
        row = idx // 4
        col = idx % 4

        # Label für Bildvorschau
        lbl = tk.Label(canvas_frame, image=img_tk, bg=canvas_bg_color)
        lbl.grid(row=row * 3, column=col, padx=5, pady=5)

        # Namenseingabefelder für jedes Bild
        name_entry = tk.Entry(canvas_frame, bg=entry_bg_color, fg=entry_fg_color)
        base_name = os.path.basename(file_paths_list[idx])
        name_entry.insert(0, os.path.splitext(base_name)[0])  # Setze den Standardnamen
        name_entry.grid(row=row * 3 + 1, column=col, padx=5, pady=5)
        entry_names.append(name_entry)

        # Auflösungslabel für jedes Bild
        res_label = tk.Label(canvas_frame, text=f"Resolution: {images[idx].width} x {images[idx].height}", bg=canvas_bg_color, fg=fg_color)
        res_label.grid(row=row * 3 + 2, column=col, padx=5, pady=5)
        resolution_labels.append(res_label)

        # Wenn der Benutzer den Namen ändert, soll die Auflösung aktualisiert werden
        name_entry.bind("<KeyRelease>", lambda event, idx=idx: update_resolution_display(idx))

    # Update the scroll region of the canvas
    canvas.update_idletasks()  # Ensure canvas content is updated
    canvas.configure(scrollregion=canvas.bbox("all"))

def update_resolution_display(index):
    if images and 0 <= index < len(images):
        width, height = images[index].size
        resolution_labels[index].config(text=f"Resolution: {width} x {height}")

def resize_images():
    if images:
        try:
            width = int(entry_width.get())
            height = int(entry_height.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for width and height.")
            return

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

# Setze die Standardgröße des Fensters
root.geometry(f"{DEFAULT_WIDTH}x600")  # Breite 1024px, Höhe 600px

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
# Canvas und Scrollbars
canvas = tk.Canvas(root, bg=canvas_bg_color)
scroll_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

# Layout für die Buttons und Eingabefelder
controls_frame = tk.Frame(root, bg=bg_color)
controls_frame.grid(row=0, column=0, sticky="nsw")

btn_select = tk.Button(controls_frame, text="Select Images", command=select_images, bg=btn_bg_color, fg=btn_fg_color)
btn_select.grid(row=0, column=0, pady=10)

label_width = tk.Label(controls_frame, text="Width:", bg=bg_color, fg=fg_color)
label_width.grid(row=1, column=0)

entry_width = tk.Entry(controls_frame, bg=entry_bg_color, fg=entry_fg_color)
entry_width.grid(row=1, column=1)

label_height = tk.Label(controls_frame, text="Height:", bg=bg_color, fg=fg_color)
label_height.grid(row=2, column=0)

entry_height = tk.Entry(controls_frame, bg=entry_bg_color, fg=entry_fg_color)
entry_height.grid(row=2, column=1)

btn_resize = tk.Button(controls_frame, text="Resize & Save All", command=resize_images, bg=btn_bg_color, fg=btn_fg_color)
btn_resize.grid(row=3, column=0, columnspan=2, pady=10)


# Layout Konfiguration
canvas.grid(row=0, column=1, sticky="nsew")
scroll_x.grid(row=1, column=1, sticky="ew")
scroll_y.grid(row=0, column=2, sticky="ns")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
