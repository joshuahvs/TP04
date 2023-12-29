from tkinter import *
from tkinter import messagebox # import tkinter dan juga messagebox 

from datetime import datetime #untuk fitur bonus


# Class untuk tampilan awal
class Display:
    # Inisiasi awal dan mengatur title window dan geometry
    def __init__(self, master):
        self.master = master
        master.title("EAN-13")
        master.geometry("400x500")
        self.homepage()

    # Fungsi yang akan menampilkan display awal
    def homepage(self):
        # Label ps file
        ps_file_label = Label(self.master, text="Save Barcode to PS file [eg: EAN13.eps]:")
        ps_file_label.pack()
        # Entry untuk memasukkan nama file
        self.ps_file_entry = Entry(self.master)
        self.ps_file_entry.pack()
        # Label untuk angka
        number_label = Label(self.master, text="Enter code (first 12 decimal digits):")
        number_label.pack()
        # Fungsi untuk memasukkan angka dan jika ditekan enter, maka barcode akan tergenerate
        self.number_entry = Entry(self.master)
        self.number_entry.bind("<Return>", self.check_input_file)
        self.number_entry.pack()

        history_button = Button(self.master, text="View History", command=self.display_history)
        history_button.pack()

        # Canvas untuk menggambarkan barcodenya
        self.canvas = Canvas(self.master, height="400", width="500", bg="white")
        self.canvas.pack()


# Class untuk memproses dan menampilakan barcode
class Barcode(Display):
    # Inisiasi awal
    def __init__(self, master):
        super().__init__(master)
        self.barcode_history = []  # List untuk menyimpan history barcode (fitur bonus)

    # Fungsi yang akan menvalidasi input file
    def check_input_file(self, event):
        file_name = self.ps_file_entry.get()
        if file_name[-4:] != ".eps":
            messagebox.showerror('Wrong input!', 'Please enter a valid postscript file')
        else:
            try:
                if open(file_name, 'r'):
                    messagebox.showerror('Wrong input!', 'File already exists')
            except:
                self.check_input_number(file_name)

    # Fungsi yang akan memvalidasi input angka
    def check_input_number(self,file_name):
        try:
            num = int(self.number_entry.get())
        except ValueError:
            messagebox.showerror('Wrong input!', 'Enter an integer number')
        num_length = len(str(num))
        if num_length != 12:
            messagebox.showerror('Wrong input!', 'The input must be a 12 digit number')
        else:
            self.check_digit(num)
            self.canvas.update()
            self.canvas.postscript(file = file_name, colormode = "color")

            check_digit = self.check_digit(num)
            # Menambahkan daftar histori barcode
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.barcode_history.append({
            'number': num,
            'filename': file_name,
            'check_digit': check_digit,
            'timestamp': timestamp
        })

    # Fungsi untuk check digit
    def check_digit(self, number):
        digits = [int(digit) for digit in str(number)] # konversi digit jadi list str
        checksum = 0
        # Mengiterasi setiap digit
        for i, digit in enumerate(digits[::-1]):
            weight = 3 if i % 2 == 0 else 1 # Menghitung weightnya berdasarkan ganjil genapnya
            checksum += digit * weight  # Menambahkan hasil perkalian ke checksum
        # Menghitung check digitnya
        check_digit = (10 - (checksum % 10)) % 10
        full_number = str(number) + str(check_digit)
        # Memanggil fungsi berikutnya
        self.display_check_digit(check_digit)
        self.display()
        self.bits(full_number)
        return check_digit

    # Fungsi untuk menampilakan histori barcode yang tergenerate (Fitur Bonus)
    def display_history(self):
        history_window = Toplevel(self.master)
        history_window.title("Barcode History")
        for barcode_info in self.barcode_history:
            label_text = f"Barcode: {barcode_info['number']} | Check Digit: {barcode_info['check_digit']} | Filename: {barcode_info['filename']} | Time: {barcode_info['timestamp']}"
            Label(history_window, text=label_text).pack()
    
    # Fungsi yang menampilkan Check digitnya
    def  display_check_digit(self, check_digit):
        self.canvas.delete('checkdigit')
        self.canvas.create_text(200, 340, fill='orange',text=f'Check Digit: {check_digit}', font='Helvetica 24 bold', tag="checkdigit")

    # Fungsi yang menampilkan untuk menampilkan teks "EAN-13 Barcode:"
    def display(self):
        self.canvas.delete('textawal')
        self.canvas.create_text(200, 35, text="EAN-13 Barcode: ", fill='black', font='Helvetica 24 bold', tag = 'textawal')

    # Fungsi untuk encoding angka yang diinput user menjadi bits
    def bits(self, number):
        #Dictionary struktur, untuk proses encodingnya
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

        # membuat angka yang diinput menjadi bits yang sesuai dengan ketentuan
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
        # Membagi bits untuk depan dan belakang
        first_6_bits = bits[:42]
        last_6_bits = bits[42:]
        self.make_barcode(start_bits, first_6_bits, middle_bits, last_6_bits, end_bits, number)

    # Fungsi yang akan membuat dan menampilakan barcodenya
    def make_barcode(self, start, first, middle, last, end, number):
        # Membagi angka
        first_digit = number[0]
        first_6 = str(number[1:7])
        last_6 =  number[7:]
        # Mengukur letak barcode agar sesuai dengan canvas
        self.canvas.delete('barcode')
        canvas_width = 280
        canvas_height = 350
        x_position = canvas_width * 0.25  # posisi mulai 25% dari width canvas
        y_start = canvas_height * 0.2  # Posisi mulai 20% dari height canvas
        y_end = canvas_height * 0.8  # Posisi berhenti 80% of dari tinggi canvas
        x_position_digit = canvas_width * 0.27 # Posisi khusus untuk angkanya
        
        self.canvas.create_text(x_position - 8, 295, text=first_digit, fill='black', font='Helvetica 24 bold', tag = 'barcode')
        # Mengiterasi untuk bit bagian start
        for bit in start:
            bit = int(bit)
            if bit == 1:
                # Menggambar barcodenya jika bit adalah 1 
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), y_end, fill='blue', outline='blue', width=0, tag='barcode')
            # Menambah posisi x agar berpindah kesamping
            x_position += canvas_width * 0.01  

        # Mengiterasi untuk bit dari 6 angka pertama
        counter = 0
        index = 0
        for bit in first:
            bit = int(bit)
            counter += 1
            if bit == 1:
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), canvas_height*0.75, fill='black', outline='black', width=0, tag='barcode')
            # Jika sudah mengiterasi 7 bit, maka akan menampilkan angka (karena 1 angka di ubah menjadi 7 bit)
            if counter % 7 == 0:
                try:
                    self.canvas.create_text(x_position_digit, 295, text=first_6[index], fill='black', font='Helvetica 24 bold', tag = 'barcode')
                    index += 1
                except IndexError:
                    pass
            x_position += canvas_width * 0.01 
            x_position_digit += canvas_width * 0.01

        # Mengiterasi untuk bagian tengah
        for bit in middle:
            bit = int(bit)
            if bit == 1:
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), y_end, fill='blue', outline='blue', width=0, tag='barcode')
            x_position += canvas_width * 0.01 
        
        # Mengiterasi untuk bagian bit dari 6 digit terakhir
        counter = 0
        index = 0
        x_position_digit += 10
        for bit in last:
            bit = int(bit)
            counter += 1
            if bit == 1:
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), canvas_height*0.75, fill='black', outline='black', width=0, tag='barcode')
            if counter % 7 == 0:
                try:
                    self.canvas.create_text(x_position_digit, 295, text=last_6[index], fill='black', font='Helvetica 24 bold', tag = 'barcode')
                    index += 1
                except IndexError:
                    pass
            x_position += canvas_width * 0.01 
            x_position_digit += canvas_width * 0.01
        
        # Mengiterasi untuk bagian paling akhir
        for bit in end:
            bit = int(bit)
            if bit == 1:
                self.canvas.create_rectangle(x_position, y_start, x_position + (canvas_width * 0.01), y_end, fill='blue', outline='blue', width=0, tag='barcode')
            x_position += canvas_width * 0.01 


# Menjalankan programnya dan membuat windownya tidak resizable
def main():
    root = Tk()
    root.resizable(False,False)
    Barcode(root)
    root.mainloop()

if __name__ == "__main__":
    main()
