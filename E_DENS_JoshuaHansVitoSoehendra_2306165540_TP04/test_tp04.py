from tkinter import *
from tkinter import messagebox

PS_FILE_EXTENSION = ".eps"
VALID_NUMBER_LENGTH = 12

# Memvalidasi file yang diinput dan memunculkan pesan salah jika tidak valid.
def check_input_file(file_name, expected_error_message):
    if file_name[-4:] != PS_FILE_EXTENSION:
        try:
            raise ValueError(expected_error_message)
        except ValueError as e:
            messagebox.showerror('Wrong input!', str(e))
    else:
        try:
            with open(file_name, 'r') as f:
                f.read()
        except FileNotFoundError:
            pass
        else:
            try:
                raise ValueError("File already exists")
            except ValueError as e:
                messagebox.showerror('Wrong input!', str(e))
# Memvalidasi nomor input dan memunculkan pesan salah jika tidak valid.
def check_input_number(number, expected_error_message):
    try:
        int(number)
    except ValueError:
        try:
            raise ValueError(expected_error_message)
        except ValueError as e:
            messagebox.showerror('Wrong input!', str(e))
    else:
        if len(str(number)) != VALID_NUMBER_LENGTH:
            try:
                raise ValueError("The input must be a 12 digit number")
            except ValueError as e:
                messagebox.showerror('Wrong input!', str(e))

#  Mengujikan apakah fungsi check_input_file memunculkan pesan kesalahan untuk nama berkas yang valid.
def test_valid_file_name():
    file_name = "valid_file_name.eps"
    expected_error_message = "Please enter a valid postscript file"
    check_input_file(file_name, expected_error_message)

# Mengujikan apakah fungsi check_input_file memunculkan pesan kesalahan untuk ekstensi berkas yang tidak valid.
def test_invalid_file_extension():
    file_name = "invalid_file_extension.txt"
    expected_error_message = "Please enter a valid postscript file"
    check_input_file(file_name, expected_error_message)

#  Mengujikan apakah fungsi check_input_file memunculkan pesan kesalahan untuk berkas yang sudah ada.
def test_existing_file():
    file_name = "existing_file.eps"
    with open(file_name, 'w') as f:
        f.write("This is an existing file.")
    expected_error_message = "File already exists"
    check_input_file(file_name, expected_error_message)

# Mengujikan apakah fungsi check_input_number memunculkan pesan kesalahan untuk nomor yang valid.
def test_valid_number():
    number = 123456789012
    expected_error_message = "Enter an integer number"
    check_input_number(number, expected_error_message)

# Mengujikan apakah fungsi check_input_number memunculkan pesan kesalahan untuk nomor yang tidak valid.
def test_invalid_number():
    number = "abc"
    expected_error_message = "Enter an integer number"
    check_input_number(number, expected_error_message)

# Mengujikan apakah fungsi check_input_number memunculkan pesan kesalahan untuk nomor dengan panjang yang salah.
def test_wrong_number_length():
    number = 12345
    expected_error_message = "The input must be a 12 digit number"
    check_input_number(number, expected_error_message)

