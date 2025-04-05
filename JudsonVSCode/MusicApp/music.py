import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer App")

        # Create a frame for the PDF list
        self.pdf_list_frame = ttk.Frame(self.root)
        self.pdf_list_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a listbox to display PDF titles
        self.pdf_listbox = tk.Listbox(self.pdf_list_frame, width=40)
        self.pdf_listbox.pack(side=tk.LEFT, fill=tk.Y)

        # Create a scrollbar for the listbox
        self.scrollbar = ttk.Scrollbar(self.pdf_list_frame, orient=tk.VERTICAL, command=self.pdf_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pdf_listbox.config(yscrollcommand=self.scrollbar.set)

        # Create a frame for the PDF content
        self.pdf_content_frame = ttk.Frame(self.root)
        self.pdf_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a canvas to display PDF images
        self.canvas = tk.Canvas(self.pdf_content_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind the listbox selection event to the handler function
        self.pdf_listbox.bind("<<ListboxSelect>>", self.display_pdf_content)

        # Load PDFs from the selected folder
        self.load_pdfs()

    def load_pdfs(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                self.pdf_listbox.insert(tk.END, pdf_file)
            self.folder_path = folder_path

    def display_pdf_content(self, event):
        selected_index = self.pdf_listbox.curselection()
        if selected_index:
            selected_pdf = self.pdf_listbox.get(selected_index)
            pdf_path = os.path.join(self.folder_path, selected_pdf)
            self.show_pdf(pdf_path)

    def show_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # Load the first page
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_tk = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk  # Keep a reference to avoid garbage collection

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewerApp(root)
    root.mainloop()