from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from DiskErasure import *

printer = test_printer_connection(VENDOR_ID, PRODUCT_ID)

class DiskErasureUI(Tk):

    def __init__(self):
        super().__init__()
        self.title("Disk Erasure Certificate Generator")
        self.geometry("350x100")  # Optional: starting size

        # Configure grid for the window
        self.grid_rowconfigure(0, weight=1)  # top space
        self.grid_rowconfigure(1, weight=0)  # input frame
        self.grid_rowconfigure(2, weight=0)  # gap
        self.grid_rowconfigure(3, weight=1)  # Print button fills remaining
        self.grid_columnconfigure(0, weight=1)  # center horizontally

        # Input Frame (Entry + Import Button)
        inputFrame = Frame(self)
        inputFrame.grid(row=1, column=0)

        self.filename = StringVar()
        filenameInput = Entry(inputFrame, width=30, textvariable=self.filename)
        filenameFind = ttk.Button(inputFrame, text="Import PDF...", width=10, command=self.import_pdf_file)

        filenameInput.grid(row=0, column=0, padx=(0, 10))
        filenameFind.grid(row=0, column=1)

        # Print button filling rest of space
        printButton = ttk.Button(self, text="Print", width=40, command=self.convert_and_print)
        printButton.grid(row=2, column=0)  # fills horizontally & vertically

    def import_pdf_file(self, *args, **kwargs):
        file = filedialog.askopenfilename(
            title="Select a PDF file",
            defaultextension=".pdf",
            initialdir="C:\\Users\\TAZW\\certificates\\",
            filetypes=[("PDF Files", "*.pdf")]  # Restrict to PDF only
        )

        self.filename.set(file)

    def convert_and_print(self):
        contents = extract_killdisk_pdf(self.filename.get())

        try:
            print_killdisk_receipt(printer, contents)

        except Exception as e:
            messagebox.showerror(title="Error Processing Certificate", message="An error occured when trying to process and print this certificate. Please try power cycling the receipt printer and try again.\n\n" + str(e))

if __name__ == "__main__":
    app = DiskErasureUI()
    app.mainloop()
