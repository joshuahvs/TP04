from tkinter import *
from tkinter import messagebox

class Display:
    def __init__(self, master):
        self.master = master

        master.title("EAN-13")
        master.geometry("400x500")
        self.homepage()

    def homepage(self):
        ps_file_label = Label(self.master, text="Save Barcode to PS file [eg: EAN13.eps]:")
        ps_file_label.pack()

        self.ps_file_entry = Entry(self.master)
        self.ps_file_entry.pack()

        number_label = Label(self.master, text="Enter code (first 12 decimal digits):")
        number_label.pack()

        self.number_entry = Entry(self.master)
        self.number_entry.bind("<Return>", self.check_input_file)
        self.number_entry.pack()

        self.canvas = Canvas(self.master, height="400", width="500", bg="white")
        self.canvas.pack()

        # self.save_as_png = Button(self.master, text='Click to save as PNG')
        # self.save_as_png.pack()

class Barcode(Display):
    def __init__(self, master):
        super().__init__(master)

    def check_input_file(self, event):
        file_name = self.ps_file_entry.get()
        if file_name[-3:] != "eps":
            messagebox.showerror('Wrong input!', 'Please enter a valid postscript file')
        try:
            if open(file_name, 'r'):
                messagebox.showerror('Wrong input!', 'File already exists')
        except:
            self.check_input_number()
            self.canvas.update()
            self.canvas.postscript(file = file_name, colormode = "color")

    def check_input_number(self):
        try:
            num = int(self.number_entry.get())
        except ValueError:
            messagebox.showerror('Wrong input!', 'Enter an integer number')
        num_length = len(str(num))
        if num_length != 12:
            messagebox.showerror('Wrong input!', 'The input must be a 12 digit number')
        self.check_digit(num)

    def check_digit(self, number):
        # konversi digit jadi list str
        digits = [int(digit) for digit in str(number)]
        # Initialize checksum
        checksum = 0
        # Iterate over each digit in the barcode
        for i, digit in enumerate(digits[::-1]):
            # Multiply digit by 3 if its position is odd, otherwise by 1
            weight = 3 if i % 2 == 0 else 1
            # Add the weighted digit to the checksum
            checksum += digit * weight
        # Calculate the check digit
        check_digit = (10 - (checksum % 10)) % 10
        full_number = str(number) + str(check_digit)
        self.display_check_digit(check_digit)
        self.display()
        self.bits(full_number)
    

    def  display_check_digit(self, check_digit):
        self.canvas.delete('checkdigit')
        self.canvas.create_text(200, 340, fill='orange',text=f'Check Digit: {check_digit}', font='Helvetica 24 bold', tag="checkdigit")

    def display(self):
        self.canvas.delete('textawal')
        self.canvas.create_text(200, 35, text="EAN-13 Barcode: ", fill='black', font='Helvetica 24 bold', tag = 'textawal')

    def bits(self, number):
        structure = {"0": "LLLLLLRRRRRR",
                "1": "LLGLGGRRRRRR",
                "2": "LLGGLGRRRRRR",
                "3": "LLGGGLRRRRRR",
                "4": "LGLLGGRRRRRR",
                "5": "LGGLLGRRRRRR",
                "6": "LGGGLLRRRRRR",
                "7": "LGLGLGRRRRRR",
                "8": "LGLGGLRRRRRR",
                "9": "LGGLGLRRRRRR"}
        l_code = {"0": "0001101",
                "1": "0011001",
                "2": "0010011",
                "3": "0111101",
                "4": "0100011",
                "5": "0110001",
                "6": "0101111",
                "7": "0111011",
                "8": "0110111",
                "9": "0001011"}
        g_code = {"0": "0100111",
                "1": "0110011",
                "2": "0011011",
                "3": "0100001",
                "4": "0011101",
                "5": "0111001",
                "6": "0000101",
                "7": "0010001",
                "8": "0001001",
                "9": "0010111"}
        r_code = {"0": "1110010",
                "1": "1100110",
                "2": "1101100",
                "3": "1000010",
                "4": "1011100",
                "5": "1001110",
                "6": "1010000",
                "7": "1000100",
                "8": "1001000",
                "9": "1110100"}
        start_bits = "101"
        middle_bits = "01010"
        end_bits = "101"
        bits = ''
        first_digit = str(number)[0]
        rest_digit = str(number)[1:]
        structure_of_digit = structure[first_digit]
        for index, stc in enumerate(structure_of_digit):
            number_to_translate = rest_digit[index]
            if stc == "L":
                bits += l_code[number_to_translate]
            elif stc == "G":
                bits += g_code[number_to_translate]
            elif stc == "R":
                bits += r_code[number_to_translate]

        first_6_bits = bits[:42]
        last_6_bits = bits[42:]
        self.make_barcode(start_bits, first_6_bits, middle_bits, last_6_bits, end_bits, number)

    def make_barcode(self, start, first, middle, last, end, number):

        first_digit = number[0]
        first_6 = str(number[1:6])
        last_6 =  number[6:]

        print(first_digit)
        print(first_6)
        print(last_6)

        self.canvas.delete('barcode')
        canvas_width = 280
        canvas_height = 350
        x_position = canvas_width * 0.25  # Start at 10% of canvas width
        y_start = canvas_height * 0.2  # Start at 20% of canvas height
        y_end = canvas_height * 0.8  # End at 80% of canvas height

        x_position_digit = canvas_width * 0.25

        self.canvas.create_text(x_position - 8, 295, text=first_digit, fill='black', font='Helvetica 24 bold', tag = 'barcode')
        for bit in start:
            bit = int(bit)
            if bit == 1:
                # Create a line if the bit is 1
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), y_end, fill='blue', outline='blue', width=0, tag='barcode')
            # Move to the next x position regardless of the bit value
            x_position += canvas_width * 0.01  # Move by 1% of canvas width

        counter = 0
        index = 0
        for bit in first:
            bit = int(bit)
            counter += 1
            if bit == 1:
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), canvas_height*0.75, fill='black', outline='black', width=0, tag='barcode')
            if counter % 7 == 0:
                try:
                    self.canvas.create_text(x_position_digit, 295, text=first_6[index], fill='black', font='Helvetica 24 bold', tag = 'barcode')
                    index += 1
                except IndexError:
                    pass
            x_position += canvas_width * 0.01 
            x_position_digit += canvas_width * 0.012

        for bit in middle:
            bit = int(bit)
            if bit == 1:
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), y_end, fill='blue', outline='blue', width=0, tag='barcode')
            x_position += canvas_width * 0.01 
        
        counter = 0
        index = 0
        x_position_digit -= 10
        for bit in last:
            bit = int(bit)
            counter += 1
            if bit == 1:
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), canvas_height*0.75, fill='black', outline='black', width=0, tag='barcode')
            if counter % 7 == 0:
                try:
                    self.canvas.create_text(x_position_digit, 295, text=first_6[index], fill='black', font='Helvetica 24 bold', tag = 'barcode')
                    index += 1
                except IndexError:
                    pass
            x_position += canvas_width * 0.01 
            x_position_digit += canvas_width * 0.012
        
        for bit in end:
            bit = int(bit)
            if bit == 1:
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), y_end, fill='blue', outline='blue', width=0, tag='barcode')
            x_position += canvas_width * 0.01 
        
        # formatted_number = f"{number[:1]}  {number[1:7]}  {number[7:13]}"
        # self.canvas.create_text(canvas_width / 2, canvas_height * 0.9, text=formatted_number, font=("Helvetica", 12), fill="black")


def main():
    root = Tk()
    root.resizable(False,False)
    Barcode(root)
    root.mainloop()

if __name__ == "__main__":
    main()