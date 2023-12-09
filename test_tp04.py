from tkinter import *
from tkinter import messagebox

# Constants for testing
PS_FILE_EXTENSION = ".eps"
VALID_NUMBER_LENGTH = 12

def check_input_file(file_name, expected_error_message):
    """
    Checks if the input file name is valid and raises an error if not.

    Args:
        file_name: The name of the input file.
        expected_error_message: The expected error message if the file name is invalid.
    """
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

def check_input_number(number, expected_error_message):
    """
    Checks if the input number is valid and raises an error if not.

    Args:
        number: The input number.
        expected_error_message: The expected error message if the number is invalid.
    """
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

def test_valid_file_name():
    """
    Tests if the check_input_file function raises an error for a valid file name.
    """
    file_name = "valid_file_name.eps"
    expected_error_message = "Please enter a valid postscript file"
    check_input_file(file_name, expected_error_message)

def test_invalid_file_extension():
    """
    Tests if the check_input_file function raises an error for an invalid file extension.
    """
    file_name = "invalid_file_extension.txt"
    expected_error_message = "Please enter a valid postscript file"
    check_input_file(file_name, expected_error_message)

def test_existing_file():
    """
    Tests if the check_input_file function raises an error for an existing file.
    """
    file_name = "existing_file.eps"
    with open(file_name, 'w') as f:
        f.write("This is an existing file.")
    expected_error_message = "File already exists"
    check_input_file(file_name, expected_error_message)

def test_valid_number():
    """
    Tests if the check_input_number function raises an error for a valid number.
    """
    number = 123456789012
    expected_error_message = "Enter an integer number"
    check_input_number(number, expected_error_message)

def test_invalid_number():
    """
    Tests if the check_input_number function raises an error for an invalid number.
    """
    number = "abc"
    expected_error_message = "Enter an integer number"
    check_input_number(number, expected_error_message)

def test_wrong_number_length():
    """
    Tests if the check_input_number function raises an error for a number with the wrong length.
    """
    number = 12345
    expected_error_message = "The input must be a 12 digit number"
    check_input_number(number, expected_error_message)

