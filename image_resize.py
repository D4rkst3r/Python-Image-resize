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

# Bildformate zur Auswahl
FORMATS = [("PNG", "png"), ("JPEG", "jpeg"), ("BMP", "bmp"), ("GIF", "gif"), ("TIFF", "tiff")]

def select_images():
    """Öffnet einen Dialog zur Auswahl von Bildern und zeigt die Vorschauen an."""
    global images, img_thumbnails, file_paths_list, entry_names, resolution_labels, canvas_frame
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")])
    if file_paths:
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
    """Zeigt die Bilder in einer Rasteransicht an."""
    global canvas_frame
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
    """Aktualisiert das Auflösungslabel für das angegebene Bild."""
    if images and 0 <= index < len(images):
        width, height = images[index].size
        resolution_labels[index].config(text=f"Resolution: {width} x {height}")

def resize_images():
    """Ändert die Größe der Bilder und speichert sie im ausgewählten Verzeichnis."""
    if images:
        try:
            width = int(entry_width.get())
            height = int(entry_height.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for width and height.")
            return

        # Bestimme das Format aus der Dropdown-Auswahl
        selected_format = format_var.get()
        if not selected_format:
            messagebox.showerror("Error", "Please select an image format.")
            return

        save_dir = filedialog.askdirectory()
        if save_dir:
            for i, img in enumerate(images):
                resized_img = img.resize((width, height))

                # Konvertiere das Bild in den richtigen Modus, wenn nötig
                if selected_format == "jpeg" and img.mode in ["RGBA", "LA"]:
                    resized_img = resized_img.convert("RGB")

                # Nutze den Namen aus dem jeweiligen Eingabefeld
                new_name = entry_names[i].get() + "." + selected_format
                save_path = os.path.join(save_dir, new_name)
                
                # Speichern im gewählten Format
                resized_img.save(save_path, format=selected_format.upper())
                
            messagebox.showinfo("Success", "All images have been resized and saved.")
        else:
            messagebox.showwarning("Warning", "No directory selected.")

# GUI Setup
root = tk.Tk()
root.title("Image Resizer - Multiview with Custom Names")

# Setze die Standardgröße des Fensters
root.geometry(f"{DEFAULT_WIDTH}x600")  # Breite 1024px, Höhe 600px
root.resizable(True, True)

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

# Layout für die Buttons und Eingabefelder
controls_frame = tk.Frame(root, bg=bg_color)
controls_frame.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)

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

# Format-Auswahl
label_format = tk.Label(controls_frame, text="Format:", bg=bg_color, fg=fg_color)
label_format.grid(row=3, column=0)

format_var = tk.StringVar(value="png")  # Default Format
format_menu = tk.OptionMenu(controls_frame, format_var, *dict(FORMATS).values())
format_menu.grid(row=3, column=1, padx=5, pady=5)

btn_resize = tk.Button(controls_frame, text="Resize & Save All", command=resize_images, bg=btn_bg_color, fg=btn_fg_color)
btn_resize.grid(row=4, column=0, columnspan=2, pady=10)

# Canvas und Scrollbars
canvas = tk.Canvas(root, bg=canvas_bg_color)
scroll_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

canvas.grid(row=0, column=1, sticky="nsew")
scroll_x.grid(row=1, column=1, sticky="ew")
scroll_y.grid(row=0, column=2, sticky="ns")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
