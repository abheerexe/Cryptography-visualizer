import tkinter as tk
from tkinter import messagebox
import numpy as np

def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def prepare_playfair_key(key):
    key = ''.join(dict.fromkeys(key.upper()))
    # Replace 'J' with 'I'
    key = key.replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = [[0] * 5 for _ in range(5)]
    row = 0
    col = 0
    for letter in key:
        matrix[row][col] = letter
        col += 1
        if col == 5:
            col = 0
            row += 1
    for letter in alphabet:
        if letter not in key and letter != 'J':
            matrix[row][col] = letter
            col += 1
            if col == 5:
                col = 0
                row += 1
    return matrix

def find_letter_positions(matrix, letter):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == letter:
                return (i, j)

def playfair_cipher_encrypt(plain_text, key):
    matrix = prepare_playfair_key(key)
    encrypted_text = ""
    plain_text = plain_text.upper().replace("J", "I") 
    for i in range(0, len(plain_text), 2):
        char1 = plain_text[i]
        char2 = plain_text[i + 1] if i + 1 < len(plain_text) else 'X'
        if char1 == char2:
            char2 = 'X'
        row1, col1 = find_letter_positions(matrix, char1)
        row2, col2 = find_letter_positions(matrix, char2)
        if row1 == row2:
            encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_text += matrix[row1][col2] + matrix[row2][col1]
    return encrypted_text

def prepare_hill_key(key):
    key = key.upper().replace(" ", "")
    key_len = len(key)
    sqrt_len = int(key_len ** 0.5)
    if sqrt_len ** 2 != key_len:
        raise ValueError("Key length must be a perfect square")
    key_matrix = np.array([ord(char) - 65 for char in key]).reshape(sqrt_len, sqrt_len)
    return key_matrix

def vigenere_cipher_encrypt(plain_text, key):
    encrypted_text = ""
    key_length = len(key)
    for i in range(len(plain_text)):
        char = plain_text[i]
        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - 65
            encrypted_text += caesar_cipher_encrypt(char, shift)
        else:
            encrypted_text += char
    return encrypted_text

def encrypt_text():
    input_text = text_entry.get("1.0", "end-1c")
    selected_cipher = cipher_variable.get()
    key = key_entry.get()
    if selected_cipher == "Caesar Cipher":
        shift = int(key)
        encrypted_text = caesar_cipher_encrypt(input_text, shift)
    elif selected_cipher == "Playfair Cipher":
        encrypted_text = playfair_cipher_encrypt(input_text, key)

    else:   
        encrypted_text = "Invalid Cipher Selection"
    
    result_text.delete("1.0", "end")
    result_text.insert("1.0", encrypted_text)

# GUI Setup
root = tk.Tk()
root.title("Cryptography Project")

# Cipher Selection
tk.Label(root, text="Select Cipher:").grid(row=0, column=0, padx=10, pady=5)
cipher_options = ["Caesar Cipher", "Playfair Cipher", "Vigenère Cipher"]
cipher_variable = tk.StringVar(root)
cipher_variable.set(cipher_options[0])
cipher_dropdown = tk.OptionMenu(root, cipher_variable, *cipher_options)
cipher_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Key Entry
tk.Label(root, text="Enter Key:").grid(row=1, column=0, padx=10, pady=5)
key_entry = tk.Entry(root)
key_entry.grid(row=1, column=1, padx=10, pady=5)

# Text Input
tk.Label(root, text="Enter Text:").grid(row=2, column=0, padx=10, pady=5)
text_entry = tk.Text(root, height=5, width=50)
text_entry.grid(row=2, column=1, padx=10, pady=5)

# Encrypt Button
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_text)
encrypt_button.grid(row=3, columnspan=2, padx=10, pady=5)

# Result Display
tk.Label(root, text="Encrypted Text:").grid(row=4, column=0, padx=10, pady=5)
result_text = tk.Text(root, height=5, width=50)
result_text.grid(row=4, column=1, padx=10, pady=5)

root.mainloop()
