from tkinter import *
from tkinter import messagebox

class BarcodeGenerator:
    def __init__(self, master):
        self.master = master

        master.title("EAN-13")
        master.geometry("350x450")
        master.resizable(False, False)
        self.homepage()

    def homepage(self):
        ps_file_label = Label(self.master, text="Save Barcode to PS file [eg: EAN13.eps]:")
        ps_file_label.pack()

        self.ps_file_entry = Entry(self.master)
        self.ps_file_entry.pack()

        number_label = Label(self.master, text="Enter code (first 12 decimal digits):")
        number_label.pack()

        self.number_entry = Entry(self.master)
        self.number_entry.pack()
        self.number_entry.bind("<Return>", self.check_input_file)

        self.canvas = Canvas(self.master, height="350", width="500", bg="white")
        self.canvas.pack()


    def check_input_file(self,file_name):
        file_name = self.ps_file_entry.get()
        if file_name[-3:] != "eps":
            messagebox.showerror('Wrong input!', 'Please enter a valid postcript file')
        else:
            self.check_input_number()

    def check_input_number(self):
        try:
            num = int(self.number_entry.get())
        except ValueError:
            messagebox.showerror('Wrong input!', 'Enter an integer number')
        num_length = len(str(num))
        if num_length != 12:
            messagebox.showerror('Wrong input!', 'The input must be a 12 digit number')
        else:
            self.create_barcode()

    def create_barcode(self):
        self.canvas.create_rectangle(50, 50, 150, 150, outline="black", fill="white")

def main():
    root = Tk()
    BarcodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()