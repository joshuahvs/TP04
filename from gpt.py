import tkinter as tk
from tkinter import simpledialog, messagebox

class EAN13BarcodeGenerator(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("EAN-13 Barcode Generator")
        self.geometry("400x200")
        self.resizable(False, False)

        # Initialize variables
        self.filename = None
        self.barcode_data = None

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Button to trigger barcode generation
        generate_button = tk.Button(self, text="Generate Barcode", command=self.generate_barcode)
        generate_button.pack(pady=10)

    def generate_barcode(self):
        # Step 1: Ask for the file name
        self.get_filename()

        # Step 2: Ask for the barcode data
        self.get_barcode_data()

        # Step 3: Calculate the check digit
        check_digit = self.calculate_checkdigit(self.barcode_data)

        # Step 4: Generate barcode and save to file
        barcode_value = self.barcode_data + str(check_digit)
        self.save_barcode(barcode_value)

        # Display barcode on canvas
        self.display_barcode(barcode_value)

    def get_filename(self):
        while True:
            self.filename = simpledialog.askstring("File Name", "Enter file name for PostScript output:")
            if self.filename:
                break

    def get_barcode_data(self):
        while True:
            self.barcode_data = simpledialog.askstring("Barcode Data", "Enter 12-digit barcode:")
            if self.barcode_data and self.barcode_data.isdigit() and len(self.barcode_data) == 12:
                break
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid 12-digit numeric barcode.")

    @staticmethod
    def calculate_checkdigit(data):
        # Calculate EAN-13 check digit
        total = sum(int(digit) * (3 if i % 2 == 0 else 1) for i, digit in enumerate(reversed(data)))
        return (10 - total % 10) % 10

    def save_barcode(self, barcode_value):
        # Save to file logic
        print(f"Saving barcode {barcode_value} to file {self.filename}")

    def display_barcode(self, barcode_value):
        # Display barcode on canvas
        canvas = tk.Canvas(self, width=400, height=200)
        canvas.pack()

        # Draw barcode manually
        bar_width = 2
        total_width = len(barcode_value) * bar_width

        start_x = (canvas.winfo_reqwidth() - total_width) // 2

        for i, digit in enumerate(barcode_value):
            x = start_x + i * bar_width
            y = 0
            height = 100

            if i % 2 == 0:
                color = "black" if int(digit) == 1 else "white"
            else:
                color = "black" if int(digit) == 1 else "gray"

            canvas.create_rectangle(x, y, x + bar_width, y + height, fill=color)

if __name__ == "__main__":
    app = EAN13BarcodeGenerator()
    app.mainloop()
