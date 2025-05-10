import tkinter as tk
from tkinter import filedialog, messagebox
from process_image import process_image, process_directory  # Imports both functions

def select_file():
    """Handle single image selection and processing."""
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

def process_folder():
    """Handle batch processing of all images in a selected folder."""
    input_dir = filedialog.askdirectory(title="Select Folder with Images to Process")
    if not input_dir:
        return

    output_dir = filedialog.askdirectory(title="Select Folder to Save Processed Images")
    if not output_dir:
        return

    try:
        processed, skipped = process_directory(input_dir, output_dir)
        messagebox.showinfo("Done", f"Processed: {processed} image(s)\nSkipped: {skipped} image(s)")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
app = tk.Tk()
app.title("Product Image Processor")
app.geometry("400x200")

btn1 = tk.Button(app, text="Process Single Image", command=select_file, font=("Arial", 14))
btn1.pack(pady=10)

btn2 = tk.Button(app, text="Process Folder of Images", command=process_folder, font=("Arial", 14))
btn2.pack(pady=10)

app.mainloop()
