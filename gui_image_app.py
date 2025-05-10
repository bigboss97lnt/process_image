import tkinter as tk
from tkinter import filedialog, messagebox
from process_image import process_image  # Imports your logic

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")]
    )
    if file_path:
        output_path = filedialog.asksaveasfilename(
            title="Save Processed Image As",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("WEBP", "*.webp")]
        )
        if output_path:
            try:
                process_image(file_path, output_path)
                messagebox.showinfo("Success", f"Image processed and saved to:\n{output_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Product Image Processor")
app.geometry("400x200")

btn = tk.Button(app, text="Select Image to Process", command=select_file, font=("Arial", 14))
btn.pack(expand=True)

app.mainloop()
