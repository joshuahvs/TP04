from tkinter import *
from tkinter import messagebox

class BarcodeGenerator:
    def __init__(self, master):
        self.master = master

        master.title("EAN-13")
        master.geometry("350x450")
        # master.resizable(False, False)
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

    def create_barcode(self, bits):
        self.canvas.delete("all")
        self.display_barcode(bits)
        # self.draw_digit_code(number)
        # self.check_digit(number)


    def display_barcode(self, binary):
        for i in range(95):
            if binary[i] == 1:
                if self.special_position(i):
                    self.special_rectange(i)
                else:
                    self.draw_rectangle(i)
            else:
                pass

    def special_position(self, number):
        if number < 3:
            return True
        elif 46 < number < 50:
            return True
        elif 91 < number < 95:
            return True
        else:
            return False

    def draw_rectangle(self, i):
        self.canvas.create_line((75 + i * 4, 80, 80 + i * 4, 210), fill='black', width=0)

    def special_rectange(self, i):
        self.canvas.create_line((100 + i * 5, 50, 110 + i * 5, 200), fill='blue', outline='blue', width=0)

    # def draw_digit_code(self):
    #     pass

    # def check_digit(self):
    #     pass


class Encoding:
    structure_first = {0: "LLLLLL",
                 1: "LLGLGG",
                 2: "LLGGLG",
                 3: "LLGGGL",
                 4: "LGLLGG",
                 5: "LGGLLG",
                 6: "LGGGLL",
                 7: "LGLGLG",
                 8: "LGLGGL",
                 9: "LGGLGL"}
    structure_last = {0: "RRRRRR",
                 1: "RRRRRR",
                 2: "RRRRRR",
                 3: "RRRRRR",
                 4: "RRRRRR",
                 5: "RRRRRR",
                 6: "RRRRRR",
                 7: "RRRRRR",
                 8: "RRRRRR",
                 9: "RRRRRR"}
    l_code = {0: "0001101",
              1: "0011001",
              2: "0010011",
              3: "0111101",
              4: "0100011",
              5: "0110001",
              6: "0101111",
              7: "0111011",
              8: "0110111",
              9: "0001011"}
    g_code = {0: "0100111",
              1: "0110011",
              2: "0011011",
              3: "0100001",
              4: "0011101",
              5: "0111001",
              6: "0000101",
              7: "0010001",
              8: "0001001",
              9: "0010111"}
    r_code = {0: "1110010",
              1: "1100110",
              2: "1101100",
              3: "1000010",
              4: "1011100",
              5: "1001110",
              6: "1010000",
              7: "1000100",
              8: "1001000",
              9: "1110100"}
    
    start_bits = "101"
    middle_bits = "01010"
    end_bits = "101"
    
    def bits_first(self, number):
        structure = self.structure_first[number]
        first_bits = ""
        for i in structure:
            if i == "L":
                bits += self.l_code[number]
            elif i == "G":
                bits += self.g_code[number]
        return first_bits
    
    def bits_first(self, number):
        structure = self.structure_last[number]
        last_bits = ""
        for i in structure:
            if i == "R":
                bits += self.r_code[number]
        return last_bits
    
class EAN_13(Encoding):
    def __init__(self) -> None:
        super().__init__()

    def full_bits(self, number):
        start_bits = super().start_bits
        first_bits = super().bits_first(number)
        middle_bits = super().middle_bits
        last_bits = super().bits_last(number)
        end_bits = super().end_bits
        full_bits = start_bits + first_bits + middle_bits + last_bits + end_bits
        return full_bits


def main():
    root = Tk()
    root.resizable(False,False)
    BarcodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()