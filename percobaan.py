bits = "000110101011110001001010000100110110001101111001010011101001110111001011100101001000"

first_6 = bits[:6]
last_6 = bits[6:12]

print("First 6 bits:", first_6)
print("Last 6 bits:", last_6)

def bits(self, number):
    # ... (Your existing code for bits function remains unchanged)

def make_barcode(self, start_bits, first_6, middle_bits, last_6, end_bits):
    # Assuming self.canvas is your canvas object

    # Function to draw a line with custom height and width
    def draw_line(x1, y1, x2, y2, height=10, width=2):
        self.canvas.create_line(x1, y1, x2, y2, width=width)
        # Draw a taller line for start, middle, and end bits
        self.canvas.create_line(x1, y1-height, x2, y2-height, width=width)

    # Draw the start bits
    draw_line(10, 50, 10, 150)  # Example coordinates, adjust as needed
    self.draw_line(10, 50, 10, 150, height=20)  # Draw a taller line for start bits

    # Draw the first 6 bits
    x_position = 10
    for bit in first_6:
        if bit == '1':
            draw_line(x_position, 50, x_position, 150, height=15)
        x_position += 2

    # Draw the middle bits
    x_position += 10  # Adjust the starting position for middle bits
    draw_line(x_position, 50, x_position, 150)  # Example coordinates, adjust as needed
    self.draw_line(x_position, 50, x_position, 150, height=20)  # Draw a taller line for middle bits

    # Draw the last 6 bits
    x_position += 10  # Adjust the starting position for last 6 bits
    for bit in last_6:
        if bit == '1':
            draw_line(x_position, 50, x_position, 150, height=15)
        x_position += 2

    # Draw the end bits
    x_position += 10  # Adjust the starting position for end bits
    draw_line(x_position, 50, x_position, 150)  # Example coordinates, adjust as needed
    self.draw_line(x_position, 50, x_position, 150, height=20)  # Draw a taller line for end bits



#  structure = {0: "LLLLLLRRRRRR",
#                  1: "LLGLGGRRRRRR",
#                  2: "LLGGLGRRRRRR",
#                  3: "LLGGGLRRRRRR",
#                  4: "LGLLGGRRRRRR",
#                  5: "LGGLLGRRRRRR",
#                  6: "LGGGLLRRRRRR",
#                  7: "LGLGLGRRRRRR",
#                  8: "LGLGGLRRRRRR",
#                  9: "LGGLGLRRRRRR"}