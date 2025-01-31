#!/usr/bin/env python3

import sys
import argparse

# Create the parser
parser = argparse.ArgumentParser(description='Rune Cipher Swiss Army Knife')

# Add arguments for each operation
parser.add_argument('-t', '--transliterate', metavar='TEXT', help='Transliterate English text to runes')
parser.add_argument('-r', '--reverse-transliterate', metavar='RUNES', help='Transliterate runes to English text')
parser.add_argument('-a', '--atbash', metavar=('RUNES', 'SHIFT'), nargs=2, help='Decrypt runes with Atbash cipher')
parser.add_argument('-v', '--vigenere', metavar=('RUNES', 'KEY'), nargs=2, help='Decrypt runes with Vigenère cipher')
parser.add_argument('-c', '--caesar-encrypt', metavar=('TEXT', 'SHIFT'), nargs=2, help='Encrypt text with Caesar cipher')
parser.add_argument('-d', '--caesar-decrypt', metavar=('RUNES', 'SHIFT'), nargs=2, help='Decrypt runes with Caesar cipher')
parser.add_argument('-p', '--playfair', metavar=('TEXT', 'KEYWORD'), nargs=2, help='Encrypt/Decrypt text with Playfair cipher')
parser.add_argument('-b', '--brute-force', metavar='RUNES', help='Attempt brute force decryption on runes')
parser.add_argument('-f', '--frequency-analysis', metavar='CIPHERTEXT', help='Perform frequency analysis on the ciphertext')
# ... Add more arguments as needed

# Parse the arguments
args = parser.parse_args()

# Ensure you have NLTK data downloaded:
# import nltk
# nltk.download('words')
import nltk

# Function to check and download necessary NLTK data
def setup_nltk():
    try:
        # Check if 'words' corpus is available
        nltk.data.find('corpora/words')
    except LookupError:
        # If not available, download 'words' corpus
        print("Downloading the 'words' corpus from NLTK, please wait...")
        nltk.download('words')
        print("'words' corpus downloaded.")

# Call the setup function at the beginning of the script
setup_nltk()

from collections import Counter

# Function to calculate letter frequencies in the text
def calculate_frequencies(text):
    # Remove non-alphabetic characters and convert to uppercase
    text = ''.join(filter(str.isalpha, text.upper()))
    # Calculate the frequency of each letter
    frequencies = Counter(text)
    total = sum(frequencies.values())
    # Convert counts to percentages
    frequencies = {letter: count / total for letter, count in frequencies.items()}
    return frequencies

import itertools
import string
from sympy import isprime, primerange
from nltk.corpus import words
from nltk.metrics.distance import edit_distance
from math import gcd

def get_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return ' '.join(lines)

# Mapping of runes to decimal values based on the provided table
rune_to_decimal = {
    'ᚠ': 0, 'ᚢ': 1, 'ᚦ': 2, 'ᚩ': 3, 'ᚱ': 4, 'ᚳ': 5, 'ᚷ': 6, 'ᚹ': 7, 'ᚻ': 8, 'ᚾ': 9, 'ᛁ': 10, 'ᛄ': 11,
    'ᛇ': 12, 'ᛈ': 13, 'ᛉ': 14, 'ᛋ': 15, 'ᛏ': 16, 'ᛒ': 17, 'ᛖ': 18, 'ᛗ': 19, 'ᛚ': 20, 'ᛝ': 21, 'ᛟ': 22,
    'ᛞ': 23, 'ᚪ': 24, 'ᚫ': 25, 'ᚣ': 26, 'ᛡ': 27, 'ᛠ': 28
}
decimal_to_rune = {v: k for k, v in rune_to_decimal.items()}

# Dictionary mapping Elder Futhark runes to English letters
futhark_to_english = {
    'ᚠ': 'F', 'ᚢ': 'U', 'ᚦ': 'TH', 'ᚩ': 'O', 'ᚱ': 'R', 'ᚳ': 'C', 'ᚷ': 'G',
    'ᚹ': 'W', 'ᚻ': 'H', 'ᚾ': 'N', 'ᛁ': 'I', 'ᛄ': 'J', 'ᛇ': 'EO', 'ᛈ': 'P',
    'ᛉ': 'X', 'ᛋ': 'S', 'ᛏ': 'T', 'ᛒ': 'B', 'ᛖ': 'E', 'ᛗ': 'M', 'ᛚ': 'L',
    'ᛝ': 'NG', 'ᛟ': 'OE', 'ᛞ': 'D', 'ᚪ': 'A', 'ᚫ': 'AE', 'ᚣ': 'Y', 'ᛡ': 'IA',
    'ᛠ': 'EA'
}

# Reverse mapping for English transliteration to runes
english_to_futhark = {v: k for k, v in futhark_to_english.items()}

def print_usage_guide():
    print("Welcome to the Rune Cipher Swiss Army Knife!")
    print("This tool allows you to perform various cipher operations with runes.")
    print("\nUsage:")
    print("1. Transliterate English to Runes: Provide English text to convert it into runes.")
    print("2. Transliterate Runes to English: Provide runes to convert them back to English text.")
    print("3. Decrypt Runes with Atbash Cipher: Provide runes and a shift value to decrypt using the Atbash cipher.")
    print("4. Decrypt Runes with Vigenère Cipher: Provide runes and a key to decrypt using the Vigenère cipher.")
    print("5. Encrypt Text with Caesar Cipher: Provide text and a shift value to encrypt using the Caesar cipher.")
    print("6. Decrypt Text with Caesar Cipher: Provide encrypted text and a shift value to decrypt.")
    print("7. Encrypt Text with Playfair Cipher: Provide text and a keyword for the Playfair cipher.")
    print("8. Decrypt Text with Playfair Cipher: Provide text and a keyword for the Playfair cipher.")
    print("9. Brute-force Decryption with Prime Shifts: Provide runes to attempt brute-force decryption.")
    print("10. Brute-force Decryption with User-Provided Key (Vigenère Cipher): Provide runes and a key to decrypt using the Vigenère cipher.")
    print("11. Attempt All Brute Force Methods (Decryption): Provide runes to attempt all brute force decryption methods.")
    print("12. Perform Frequency Analysis on Ciphertext")
    print("13. Attempt All Brute Force Methods with Primes (Decryption)")
    print("\nYou can also use command-line arguments to directly perform operations without the interactive menu.")
    print("For example:")
    print("python rune_cipher_tool.py --transliterate 'Hello World'")
    print("python rune_cipher_tool.py --atbash 'ᚦᛖ-ᛚᚩᛋᛋ-ᚩᚠ-ᛞᛁᚢᛁᚾᛁᛏᚣ' 5")
    print("\nFor more information on command-line arguments, use the --help flag.")
    print("python rune_cipher_tool.py --help")

# Function to perform frequency analysis on the ciphertext
def frequency_analysis(ciphertext):
    frequencies = calculate_frequencies(ciphertext)
    # Sort the frequencies in descending order
    sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
    # Print the frequencies
    print("Letter frequencies in the ciphertext:")
    for letter, frequency in sorted_frequencies:
        print(f"{letter}: {frequency:.2%}")

# Function to transliterate text to runes
def transliterate_to_futhark(text):
    # Create the reverse mapping from English to runes
    english_to_futhark = {v: k for k, v in futhark_to_english.items()}
    # Convert the text to uppercase to match the keys in the dictionary
    text = text.upper()
    # Transliterate the text to runes
    transliterated_text = ''
    for char in text:
        if char in english_to_futhark:
            transliterated_text += english_to_futhark[char]
        else:
            transliterated_text += char  # Non-mapped characters are kept as is
    return transliterated_text

# Function to transliterate runes to English and replace hyphens with spaces
def transliterate_futhark(runes):
# Convert the runes from Elder Futhark to English
    transliterated_text = ''
    for rune in runes:
        if rune in futhark_to_english:
            transliterated_text += futhark_to_english[rune]
        else:
            transliterated_text += rune  # Non-mapped characters are kept as is
    return transliterated_text

#Function to transliterate and convert
def transliterate_and_convert(runes):
    # Use the existing function to transliterate runes to English
    english_text = transliterate_futhark(runes)
    # Convert runes to decimal values
    decimal_values = [str(rune_to_decimal.get(rune, '?')) for rune in runes]
    # Return both the English transliteration and decimal values
    return english_text, decimal_values

# Example usage:
runes = "ᚦᛖ-ᛚᚩᛋᛋ-ᚩᚠ-ᛞᛁᚢᛁᚾᛁᛏᚣ.ᚦᛖ-ᚳᛁᚱᚳᚢ"
english_text, decimal_values = transliterate_and_convert(runes)
print(f"Transliterated English text: {english_text}")
print(f"Decimal values: {' '.join(decimal_values)}")

# Function to decrypt Atbash cipher
def decrypt_atbash(ciphertext, shift=0):
    # Decrypt the ciphertext using the Atbash cipher method
    decrypted_text = ""
    for rune in ciphertext:
        if rune in rune_to_decimal:
            # Apply the Atbash cipher transformation
            decrypted_value = 28 - rune_to_decimal[rune]
            # Apply the shift
            decrypted_value = (decrypted_value + shift) % 29
            # Map the decrypted value back to a rune
            decrypted_text += decimal_to_rune.get(decrypted_value, '?')
        else:
            # Preserve non-rune characters (such as '-', '/')
            decrypted_text += rune
    return decrypted_text

# Function to decrypt Vigenère cipher
def decrypt_vigenere(ciphertext, key, skip_indices):
    # Convert key to decimal values
    key_decimal = [rune_to_decimal[rune] for rune in key if rune in rune_to_decimal]
    decrypted_text = ""
    key_index = 0

    for index, rune in enumerate(ciphertext):
        if index in skip_indices or rune not in rune_to_decimal:
            decrypted_text += rune
        else:
            # Apply the Vigenère cipher transformation
            decrypted_value = (rune_to_decimal[rune] - key_decimal[key_index]) % 29
            decrypted_text += decimal_to_rune.get(decrypted_value, '?')
            key_index = (key_index + 1) % len(key_decimal)

    return decrypted_text

# Caesar Cipher Encryption and Decryption
def encrypt_caesar(plaintext, shift):
    # Encrypt the plaintext using the Caesar cipher method
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return plaintext.translate(table)

def decrypt_caesar(ciphertext, shift):
    # Decrypt the ciphertext using the Caesar cipher method
    return encrypt_caesar(ciphertext, -shift)

# Playfair Cipher Key Generation, Encryption, and Decryption
def generate_playfair_key(keyword):
    # Generate the 5x5 key matrix for Playfair cipher
    matrix = []
    alphabet = 'abcdefghiklmnopqrstuvwxyz'  # 'j' is usually excluded in Playfair
    used_chars = set()

    # Add keyword to the matrix
    for char in keyword.lower():
        if char not in used_chars and char in alphabet:
            matrix.append(char)
            used_chars.add(char)

    # Fill the rest of the matrix with the remaining alphabet
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)

    return matrix

def split_into_digraphs(plaintext):
    # Split the plaintext into digraphs for Playfair cipher
    plaintext = plaintext.lower().replace('j', 'i')  # 'j' is usually replaced with 'i'
    digraphs = []

    i = 0
    while i < len(plaintext):
        digraph = plaintext[i]
        i += 1
        if i < len(plaintext) and plaintext[i] != digraph:
            digraph += plaintext[i]
            i += 1
        else:
            digraph += 'x'  # Padding character if needed
        digraphs.append(digraph)

    return digraphs

def find_position(char, matrix):
    # Find the position of a character in the key matrix
    index = matrix.index(char)
    return index // 5, index % 5  # Row, Column

def encrypt_playfair(plaintext, keyword):
    # Encrypt the plaintext using the Playfair cipher method
    matrix = generate_playfair_key(keyword)
    digraphs = split_into_digraphs(plaintext)
    ciphertext = ''

    for digraph in digraphs:
        row1, col1 = find_position(digraph[0], matrix)
        row2, col2 = find_position(digraph[1], matrix)

        if row1 == row2:  # Same row
            ciphertext += matrix[row1 * 5 + (col1 + 1) % 5]
            ciphertext += matrix[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:  # Same column
            ciphertext += matrix[((row1 + 1) % 5) * 5 + col1]
            ciphertext += matrix[((row2 + 1) % 5) * 5 + col2]
        else:  # Rectangle
            ciphertext += matrix[row1 * 5 + col2]
            ciphertext += matrix[row2 * 5 + col1]

    return ciphertext

def decrypt_playfair(ciphertext, keyword):
    # Decrypt the ciphertext using the Playfair cipher method
    keyword = keyword.replace(' ', '')
    # Generate the 5x5 key matrix for Playfair cipher
    matrix = generate_playfair_key(keyword)
    digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    plaintext = ''

    for digraph in digraphs:
        row1, col1 = find_position(digraph[0], matrix)
        row2, col2 = find_position(digraph[1], matrix)

        if row1 == row2:  # Same row
            plaintext += matrix[row1 * 5 + (col1 - 1) % 5]
            plaintext += matrix[row2 * 5 + (col2 - 1) % 5]
        elif col1 == col2:  # Same column
            plaintext += matrix[((row1 - 1) % 5) * 5 + col1]
            plaintext += matrix[((row2 - 1) % 5) * 5 + col2]
        else:  # Rectangle
            plaintext += matrix[row1 * 5 + col2]
            plaintext += matrix[row2 * 5 + col1]

    return plaintext

# Function to generate prime numbers within a range
def generate_primes(start, end):
    return list(primerange(start, end))

# Function to calculate Euler's totient function
def euler_totient(n):
    if n == 1:
        return 1
    else:
        phi = 1
        for i in range(2, n):
            if gcd(n, i) == 1:
                phi += 1
        return phi

# Function to calculate the Greatest Common Divisor (Euclid's algorithm)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Function to check for English coherence with a threshold for unrecognized words
def is_coherent(text, threshold=0.25):
    english_vocab = set(words.words())
    text_words = text.replace('-', ' ').replace('.', ' ').split()  # Split compound words and sentences
    recognized_words = [word.lower() for word in text_words if word.lower() in english_vocab]
    coherence_ratio = len(recognized_words) / len(text_words)
    # Alert the user if the text is coherent based on the threshold
    if coherence_ratio >= threshold:
        print("The transliterated text is mostly coherent in English.")
        return True
    return False

# Function to calculate the edit distance to English words
def englishness_score(text):
    english_vocab = set(words.words())
    text_words = text.split()
    distances = [edit_distance(word.lower(), best_match(word.lower(), english_vocab)) for word in text_words]
    return sum(distances)

def best_match(word, vocab):
    return min(vocab, key=lambda w: edit_distance(word, w))

# List of all decryption methods
decryption_methods = [decrypt_atbash, decrypt_vigenere, decrypt_caesar, decrypt_playfair]

# Brute-force function to try all ciphers with prime shifts
def brute_force_decrypt(runes, key=None, keyword=None):
    # Transliterate runes to English and print the transliteration
    transliterated_text = transliterate_futhark(runes)
    print(f"Transliterated text: {transliterated_text}")

    primes = generate_primes(0, 100)  # Generate prime numbers for shifts
    possible_results = []

    # Split the runes into lines for multi-line handling
    lines = runes.split('\n')

    # Process each line with brute force decryption
    for line in lines:
        for prime in primes:
            # Try Atbash with prime shift for each line and print the attempt
            atbash_result = decrypt_atbash(line, prime)
            print(f"Atbash attempt with shift {prime}: {atbash_result}")
            if is_coherent(atbash_result):
                possible_results.append((atbash_result, 'Atbash', prime))

            # Try Caesar with prime shift for each line and print the attempt
            caesar_result = decrypt_caesar(line, prime)
            print(f"Caesar attempt with shift {prime}: {caesar_result}")
            if is_coherent(caesar_result):
                possible_results.append((caesar_result, 'Caesar', prime))

        # If a key is provided, try Vigenère decryption with the user-provided key and print the attempt
        if key:
            vigenere_result = decrypt_vigenere(line, key, [])
            print(f"Vigenère attempt with key {key}: {vigenere_result}")
            if is_coherent(vigenere_result):
                possible_results.append((vigenere_result, 'Vigenère', key))

        # If a keyword is provided, try Playfair decryption with the user-provided keyword and print the attempt
        if keyword:
            playfair_result = decrypt_playfair(line, keyword)
            print(f"Playfair attempt with keyword {keyword}: {playfair_result}")
            if is_coherent(playfair_result):
                possible_results.append((playfair_result, 'Playfair', keyword))

    # If no coherent result is found for any line, return the line with the best Englishness score
    best_result = min(possible_results, key=lambda x: englishness_score(x[0]), default=("No coherent result found", "None", None))
    return best_result

def attempt_all_brute_force(runes):
    # Generate prime numbers for shifts
    primes = generate_primes(0, 100)
    possible_results = []

    # Attempt brute force for each cipher method
    for prime in primes:
        atbash_result = decrypt_atbash(runes, prime)
        if is_coherent(atbash_result):
            possible_results.append((atbash_result, 'Atbash', prime))

        caesar_result = decrypt_caesar(runes, prime)
        if is_coherent(caesar_result):
            possible_results.append((caesar_result, 'Caesar', prime))

    # Add more brute force attempts for other ciphers if available
    # ...

    # Choose the best result based on Englishness score or coherence
    best_result = min(possible_results, key=lambda x: englishness_score(x[0]), default=("No coherent result found", "None", None))
    return best_result

import tkinter as tk
from tkinter import scrolledtext

class TextHandler(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Scroll the Text widget to show the latest output

    def flush(self):
        pass  # Add this method

def main_gui():
    # Create a new window
    window = tk.Tk()
    window.title("Rune Cipher Swiss Army Knife")

    # Add a scrolled text box that will display the script output
    output_box = scrolledtext.ScrolledText(window, width=50, height=10)
    output_box.pack()

    # Create a TextHandler instance for the output box
    text_handler = TextHandler(output_box)

    # Modify the main function to write its output to the text box
    def main_output():
        # Redirect standard output to the text box
        sys.stdout = text_handler
        # Call the main function
        main()
        # Redirect standard output back to the console
        sys.stdout = sys.__stdout__

    # Add a button that calls the main_output function when clicked
    button = tk.Button(window, text="Run", command=main_output)
    button.pack()

    # Run the GUI loop
    window.mainloop()

# Main function with additional brute-force option
def main():
    # Print the usage guide at the start of the program
    print_usage_guide()

    if len(sys.argv) > 1:
        if args.transliterate:
            result = transliterate_to_futhark(args.transliterate)
            print(f"Transliterated text: {result}")

        elif args.frequency_analysis:
            frequency_analysis(args.frequency_analysis)

        elif args.reverse_transliterate:
            english_text, decimal_values = transliterate_and_convert(args.reverse_transliterate)
            print(f"Transliterated English text: {english_text}")
            print(f"Decimal values: {' '.join(decimal_values)}")

        elif args.atbash:
            runes, shift = args.atbash
            result = decrypt_atbash(runes, int(shift))
            print(f"Decrypted text: {result}")
        # ... Handle other arguments similarly

    else:
        while True:
            # Show the menu
            print("Welcome to the Rune Cipher Swiss Army Knife!")
            print("Choose an operation from the following options:")
            print("1 - Transliterate English to Runes (Transliteration)")
            print("2 - Transliterate Runes to English")
            print("3 - Decrypt Runes with Atbash Cipher (Decryption)")
            print("4 - Decrypt Runes with Vigenère Cipher (Decryption)")
            print("5 - Encrypt Text with Caesar Cipher (Encryption)")
            print("6 - Decrypt Text with Caesar Cipher (Decryption)")
            print("7 - Encrypt Text with Playfair Cipher (Encryption)")
            print("8 - Decrypt Text with Playfair Cipher (Decryption)")
            print("9 - Brute-force Decryption with Prime Shifts (Decryption)")
            print("10 - Brute-force Decryption with User-Provided Key (Vigenère Cipher)")
            print("11 - Attempt All Brute Force Methods (Decryption)")
            print("12 - Perform Frequency Analysis on Ciphertext")
            print("13 - Attempt All Brute Force Methods with Primes (Decryption)")
            choice = input("Enter your choice (1-13): ")
            if choice == 'q':
                break  # Exit the loop to end the program

            # Use a dialog box to get the user's choice
#            choice = sd.askstring("Input", "Enter your choice (1-13): ")


            elif choice == '1':
                text = get_multiline_input("Enter the English text to transliterate to runes: ")
                result = transliterate_to_futhark(text)
                print(f"Transliterated text: {result}")

            elif choice == '2':
                runes = get_multiline_input("Enter the runes to transliterate to English (end with an empty line):")
                english_text, decimal_values = transliterate_and_convert(runes)
                print(f"Transliterated English text: {english_text}")

            elif choice == '3':
                runes = get_multiline_input("Enter the runes to decrypt with Atbash: ")
                try:
                    shift = int(input("Enter the shift amount (0-28): "))
                    if not 0 <= shift <= 28:
                        raise ValueError("Shift must be between 0 and 28.")
                    result = decrypt_atbash(runes, shift)
                    print(f"Decrypted text: {result}")
                except ValueError as e:
                    print(f"Invalid input: {e}")

            elif choice == '4':
                runes = get_multiline_input("Enter the runes to decrypt with Vigenère: ")
                key = input("Enter the Vigenère key (in runes): ")
                skip_indices_input = input("Enter indices to skip (comma-separated, no spaces): ")
                skip_indices = [int(index) for index in skip_indices_input.split(',')]
                result = decrypt_vigenere(runes, key, skip_indices)
                print(f"Decrypted text: {result}")

            elif choice == '5':
                text = get_multiline_input("Enter the text to encrypt with Caesar: ")
                try:
                    shift = int(input("Enter the shift amount (0-25): "))
                    if not 0 <= shift <= 25:
                        raise ValueError("Shift must be between 0 and 25.")
                    result = encrypt_caesar(text, shift)
                    print(f"Encrypted text: {result}")
                except ValueError as e:
                    print(f"Invalid input: {e}")

            elif choice == '6':
                runes = get_multiline_input("Enter the runes to decrypt with Caesar: ")
                try:
                    shift = int(input("Enter the shift amount (0-25): "))
                    if not 0 <= shift <= 25:
                        raise ValueError("Shift must be between 0 and 25.")
                    result = decrypt_caesar(runes, shift)
                    print(f"Decrypted text: {result}")
                except ValueError as e:
                    print(f"Invalid input: {e}")

            elif choice == '7':
                text = get_multiline_input("Enter the text to encrypt with Playfair: ")
                keyword = input("Enter the keyword for the Playfair cipher: ")
                result = encrypt_playfair(text, keyword)
                print(f"Encrypted text: {result}")

            elif choice == '8':
                runes = get_multiline_input("Enter the runes to decrypt with Playfair: ")
                keyword = input("Enter the keyword for the Playfair cipher: ")
                result = decrypt_playfair(runes, keyword)
                print(f"Decrypted text: {result}")

            elif choice == '9':
                runes = get_multiline_input("Enter the runes to decrypt: ")
                key = input("Enter the Vigenère key (in runes), or press Enter to skip: ")
                keyword = input("Enter the Playfair keyword (in English), or press Enter to skip: ")
                if keyword and not all(char in rune_to_decimal for char in keyword):
                    keyword = transliterate_to_futhark(keyword)
                result, cipher, detail = brute_force_decrypt(runes, key, keyword)
                print(f"Decrypted message: {result}")
                print(f"Method used: {cipher}")
                print(f"Detail (shift, key, or keyword): {detail}")

            elif choice == '10':
                runes = get_multiline_input("Enter the runes to decrypt: ")
                key = input("Enter your key (in English or runes): ")
                if not all(char in rune_to_decimal for char in key):
                    key = transliterate_to_futhark(key)
                result = decrypt_vigenere(runes, key, [])
                print(f"Decrypted text: {result}")

            elif choice == '11':
                runes = get_multiline_input("Enter the runes to decrypt: ")
                possible_results = attempt_all_brute_force(runes)
                print(possible_results)  # Add this line here
                for result in possible_results:
                    if result is not None and len(result) == 3:
                        result, cipher, shift = result
                        print(f"Decrypted message: {result}")
                        print(f"Method used: {cipher}")
                        print(f"Shift: {shift}")
                    else:
                        print(result)

            elif choice == '12':
                runes = get_multiline_input("Enter the runes to decrypt: ")
                ciphertext = input("Enter the ciphertext to analyze: ")
                frequency_analysis(ciphertext)

            elif choice == '13':
                runes = get_multiline_input("Enter the runes to decrypt: ")
                primes = generate_primes(0, 100)  # Generate prime numbers for shifts
                for prime in primes:
                    totient = euler_totient(prime)
                    print(f"Trying prime {prime} with Euler's totient {totient}:")
                    for decrypt_method in decryption_methods:
                        # Assuming transliterate_futhark is defined elsewhere
                        transliterated_text = transliterate_futhark(runes)
                        if decrypt_method == decrypt_vigenere:
                            # Convert prime to a string
                            prime_str = str(prime)
                            decrypted_result = decrypt_method(transliterated_text, prime_str, [])
                        elif decrypt_method == decrypt_playfair:
                            # Convert prime to a string
                            prime_str = str(prime)
                            decrypted_result = decrypt_method(transliterated_text, prime_str)
                        else:
                            decrypted_result = decrypt_method(transliterated_text, prime)
                        # Assuming is_coherent is a function that checks if the result makes sense
                        if is_coherent(decrypted_result):
                            print(f"{decrypt_method.__name__} result is coherent: {decrypted_result}")
                        else:
                            print(f"{decrypt_method.__name__} result: {decrypted_result}")

# Call the main function to start the program
if __name__ == "__main__":
 # Ask the user which interface they want to use
    interface = input("Do you want to use the GUI (G) or the command-line interface (C)? ")

    if interface.lower() == 'g':
        # If the user chose the GUI, call the main_gui function
        main_gui()
    else:
        # If the user chose the command-line interface, or entered anything else, call the main function
        main()
