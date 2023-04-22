#
# Irrational number cipher
# Written by philip0000000
# Find the project here [https://github.com/philip0000000/square-root-irrational-number-cipher]
#

import os
import sys
import argparse
import math
from decimal import Decimal, getcontext

def get_n_non_square_number(n):
    """Get the Nth non square number"""
    # Proof: https://www.jstor.org/stable/3618253?seq=1
    return n + math.floor(0.5 + math.sqrt(n))

def save_sqrt_to_file(radicand, write_to_filename, number_of_precision):
    """Save square root of the radicand to a file."""
    try:
        # Check that the radicand is a valid number
        radicand = int(radicand)
        if radicand < 0:
            print("The number to square root is negative.", file = sys.stdout)
            return

        # Check that the number of precision is a valid number
        number_of_precision = int(number_of_precision)
        if number_of_precision < 0:
            print("The number of precision for square root is negative.", file = sys.stdout)
            return

        # Calculate the square root of the radicand
        getcontext().prec = number_of_precision
        root_number = Decimal(radicand).sqrt()

        # Write the square root to the file
        with open(write_to_filename, 'w') as file_write:
            file_write.write(str(root_number))
    except ValueError:
        print("ERROR!", file=sys.stderr)
        if not radicand.isnumeric():
            print("The radicand to square root contains non-numeric characters.", file=sys.stderr)
        elif not number_of_precision.isnumeric():
            print(f"The precision value for square root of {radicand} contains non-numeric characters.", file=sys.stderr)
        print(f"Writing the square root of {radicand} to the file {write_to_filename} was aborted.", file=sys.stderr)
    except OSError:
        print("ERROR!", file=sys.stderr)
        print(f"Could not write to the file: {write_to_filename}.", file=sys.stderr)
        print(f"Writing the square root of {radicand} to the file {write_to_filename} was aborted.", file=sys.stderr)

def number_of_decimal_numbers_in_file(filename_to_read):
    """Print the number of decimal numbers in the file."""
    try:
        # Read file
        with open(filename_to_read) as file:
            file_content = file.read()
        # Remove all dots
        file_content = file_content.replace('.', '')
        # Convert file content to integer
        file_content = int(file_content)

        # In base 10
        file_content_str = str(file_content)
        print(f"The number of digits(base 10) in the file {filename_to_read} is {len(file_content_str)}.", file = sys.stdout)
        # In base  16, hexadecimal
        hex_value = hex(file_content)
        print(f"The number of hexadecimal(base 16) digits in the file {filename_to_read} is {len(hex_value)-2}.", # remove 2, because 0x in the beginning
              file = sys.stdout)
    except FileNotFoundError:
        print("ERROR!", file = sys.stderr)
        print(f"Could not find the file {filename_to_read},", file = sys.stderr)
        print(f"Writing the number of characters in the file {filename_to_read} was aborted", file = sys.stderr)
def number_of_characters_in_file(filename):
    """Print the number of characters in a file."""
    try:
        with open(filename, 'r') as file:
            filename_data = file.read()
            print(f"The length of the file {filename} is {len(filename_data)}", file = sys.stdout)
    except FileNotFoundError:
        print("ERROR!", file = sys.stderr)
        print(f"Could not find the file {filename},", file = sys.stderr)
        print(f"Writing the number of characters in the file {filename} was aborted", file = sys.stderr)

def xor_file(input_file, key_file, output_file):
    try:
        # Read plain text file
        with open(input_file, 'rb') as file:
            plain_text = file.read()
        
        # Read key file
        with open(key_file) as file:
            key = file.read()
        
        # Prepare key
        key = key.replace('.', '') # Remove dots
        
        # Use bytearray to store byte values
        byte_values_output = bytearray()
        
        # XOR encrypt/decrypt each plain text with 2 hexadecimal digits in key file
        key_index = 0
        for char in plain_text:
            hex_value = int(key[key_index:key_index+2], 16)
            char = char ^ hex_value                # XOR and get new value
            byte_values_output.append(char)        # Store new value
            key_index = (key_index + 2) % len(key) # Wrap around key index
            
        # Open the file in write mode, overwriting its contents if it exists
        with open(output_file, "wb") as file:
            file.write(byte_values_output)         # Write byte values to file
    except FileNotFoundError as e:
        print(f"File not found error: {e}", file=sys.stderr)
    except PermissionError as e:
        print(f"Permission error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def get_distribution_of_tokens_in_file(filename_to_read, option = "distribution of character" , binary_mode = False):
    """Return the distribution of tokens in file."""
    # Read the file
    try:
        with open(filename_to_read, 'r' if binary_mode == False else 'rb') as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"ERROR: The file '{filename_to_read}' was not found.", file=sys.stderr)
        return {}

    if not file_content:
        print(f"ERROR: The file '{filename_to_read}' is empty!", file=sys.stderr)
        return {}

    # Check if file content is a number, if set in options
    if option == "distribution of numbers" or option == "distribution of numbers in base-16":
        # Remove all dots
        file_content = file_content.replace('.', '')
        # Check if valid number
        if is_number(file_content) == False:
            print(f"ERROR: The file '{filename_to_read}' is not a valid number!", file=sys.stderr)
            return {}

    # Convert to hex(base-16) if option is set
    if option == "distribution of numbers in base-16":
        # Convert file content to integer
        file_content = int(file_content)
        # Convert file to base-16
        file_content = hex(file_content)
        # Remove 0x from begging of string
        file_content = file_content[2:]

    # Count all tokens in the file
    tokens = {}
    for token in file_content:
        if token in tokens:
            tokens[token] += 1
        else:
            tokens[token] = 1

    # Remove escape character and tab
    if option == "distribution of character, ignore escape character and tab" or \
    option == "distribution of numbers" or option == "distribution of numbers in base-16":
        if "\t" in tokens:
            del tokens["\t"]
        if "\n" in tokens:
            del tokens["\n"]
        if "\r" in tokens:
            del tokens["\r"]

    return tokens
def print_table(data):
    if any(data):
        # Get padding for the first column
        padding = data[1].index("|") - 2
        # Print information about the file and first row
        print(data[0], file = sys.stdout)
        print(data[1], file = sys.stdout)
        # Get total value
        total = 0
        dict = data[2]
        for key, value in dict.items():
            total += value
        # Print table
        for key, value in dict.items():
            p = round(value/total, 3)
            p = str(p)
            print(f" {key:<{padding}} | {p:<5} | {value}", file = sys.stdout)
        print(f"Total numbers that occured: {total}", file = sys.stdout)

def get_distributing_of_character_compared_to_each_other(filename):
    if os.stat(filename).st_size == 0:
        raise ValueError(f"The file {filename} is empty!")

    count_data = {}
    # Count characters
    with open(filename, 'rb') as f:
        for i, c in enumerate(f.read()):
            if c not in count_data:
                count_data[c] = { "n-th_last_time_character_was_found": 0,
                                  "sum_of_value_found_distance": 0,
                                  "total_number_of_character_found": 0,
                                  "distribution_of_value": 0}
            else:
                count_data[c]["sum_of_value_found_distance"] += count_data[c]["n-th_last_time_character_was_found"]
                count_data[c]["n-th_last_time_character_was_found"] = 0
            count_data[c]["total_number_of_character_found"] += 1
            # Add +1 to all characters that have been found, except for the one that was just read
            for key, value in count_data.items():
                if (key != c):
                    value["n-th_last_time_character_was_found"] += 1
    # Calculate the percentage/fraction the value occurred, compared to total distance that value has, summed
    for key, value in count_data.items():
        value["distribution_of_value"] = value["sum_of_value_found_distance"] / value["total_number_of_character_found"]
    return count_data
def print_the_distributing_of_character_compared_to_each_other(data, filename):
    if any(data):
        print(f"File: {filename}", file = sys.stdout)
        print(" character | distribution of value | sum of value found distance | total number of character found", file = sys.stdout)
        for key, value in data.items():
            dv = round(value["distribution_of_value"], 5)
            dv = str(dv)
            svd = str(value["sum_of_value_found_distance"])
            tnf = str(value["total_number_of_character_found"])
            print(f" {key:<9} | {dv:<21} | {svd:<27} | {tnf}", file = sys.stdout)

def main():
    parser = argparse.ArgumentParser(description = "Irrational number cipher")
    parser.add_argument("-nsqrt", metavar = "<n number of square root to return>", help = "get the n-th number of non-square")
    parser.add_argument("-sqrt", nargs = 3, metavar = ("<number to sqrt>",
                        "<file name to store file in>", "<precision to calculate to>"),
                        help = "generate text file with square root to the number of precision specified")
    
    parser.add_argument("-l", metavar = "<filename>", help = "get length of file")
    parser.add_argument("-dl", metavar = "<filename>", help = "get the number of decimal numbers in the file")
 
    parser.add_argument("-e", metavar = ("<filename to encrypt>", "<filename of file with number>", "<output filename>"), nargs = 3, help = "encrypt file")
    parser.add_argument("-de", metavar = ("<filename to decrypt>", "<filename of file with number>", "<output filename>"), nargs = 3, help = "decrypt file")
    
    parser.add_argument("-b", action="store_true", help="read file in binary mode (only for use with -d, -di, -dd and -dist)")

    parser.add_argument("-d", metavar = "<filename>", help = "get distribution of character in the file")
    parser.add_argument("-di", metavar = "<filename>", help = "get distribution of character in the file and ignore escape character for tab and new line")
    parser.add_argument("-dd", metavar = "<filename>", help = "get distribution of numbers in the file")
    parser.add_argument("-dhex", metavar = "<filename>", help = "get distribution of numbers in base-16 in the file")
    parser.add_argument("-dist", metavar = "<filename>", help = "get distribution of character in file compared to each other(0 == no distrubution/all characters are in a clusters, 1 == even distrubution of character in file, X > 1 more distrubuted)")

    args = parser.parse_args()

    # Execute commands
    try:
        if args.nsqrt is not None:
            print(get_n_non_square_number(int(args.nsqrt)))
        elif args.sqrt is not None:
            save_sqrt_to_file(args.sqrt[0], args.sqrt[1], args.sqrt[2])
            
        elif args.l is not None:
            number_of_characters_in_file(args.l)
        elif args.dl is not None:
            number_of_decimal_numbers_in_file(args.dl)

        elif args.e is not None or args.de is not None:
            xor_file(args.e[0], args.e[1], args.e[2])

        elif args.d is not None:
            dict = get_distribution_of_tokens_in_file(args.d, "distribution of character", args.b)
            if bool(dict):
                data = []
                data.append(f"File: {args.d}")
                data.append("Character |   %   | Number of occurrence")
                data.append(dict)
                print_table(data)
        elif args.di is not None:
            dict = get_distribution_of_tokens_in_file(args.di, "distribution of character, ignore escape character and tab", args.b)
            if bool(dict):
                data = []
                data.append(f"File: {args.di}")
                data.append("Character |   %   | Number of occurrence")
                data.append(dict)
                print_table(data)
        elif args.dd is not None:
            dict = get_distribution_of_tokens_in_file(args.dd, "distribution of numbers", args.b)
            if bool(dict):
                data = []
                data.append(f"File: {args.dd}")
                data.append("Number |   %   | Number of occurrence")
                data.append(dict)
                print_table(data)
        elif args.dhex is not None:
            dict = get_distribution_of_tokens_in_file(args.dhex, "distribution of numbers in base-16")
            if bool(dict):
                data = []
                data.append(f"File: {args.dhex}")
                data.append("Number |   %   | Number of occurrence")
                data.append(dict)
                print_table(data)
        elif args.dist is not None:
            data = get_distributing_of_character_compared_to_each_other(args.dist)
            print_the_distributing_of_character_compared_to_each_other(data, args.dist)
    except Exception as e:
        print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
        command = os.path.basename(__file__) + ' ' + ' '.join(sys.argv[1:])
        print(f"Command executed: {command}", file = sys.stderr)

if __name__ == '__main__':
    main()
