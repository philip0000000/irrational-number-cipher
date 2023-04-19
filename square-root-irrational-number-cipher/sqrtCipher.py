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

class number_has_nonnumerical_characters_error(Exception):
    """The number has nonnumerical characters."""
    pass

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
            print("The number to square root is negative.")
            return

        # Check that the number of precision is a valid number
        number_of_precision = int(number_of_precision)
        if number_of_precision < 0:
            print("The number of precision for square root is negative.")
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

def xor_file(plain_text_file, key_file, file_to_store_cipher):
    try:
        # Read plain text file
        with open(plain_text_file, 'rb') as file:
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
            char = char ^ hex_value # XOR and get new value
            byte_values_output.append(char) # store new value
            key_index = (key_index + 2) % len(key) # wrap around key index
            
        # Open the file in write mode, overwriting its contents if it exists
        with open(file_to_store_cipher, "wb") as file:
            file.write(byte_values_output) # Write byte values to file
        
    except FileNotFoundError as e:
        print(f"File not found error: {e}", file=sys.stderr)
    except PermissionError as e:
        print(f"Permission error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

def get_distrubution_of_characters_in_file(filename_to_read, ignore_escape_characters = True):
    data_character_distrubution = {}
    find_this = []
    try:
        if os.stat(filename_to_read).st_size == 0:
            print(f"The file {filename_to_read} is empty!")
        else:
            # Initialize the dictionary with key of total amount of characters
            data_character_distrubution["total_amount_of_characters"] = 0
        
            # Count characters
            with open(filename_to_read) as f:
                while True:
                    # Read from file
                    c = f.read(1)
                    if not c:
                        break
                    if c in find_this:
                        data_character_distrubution[f"occurrence_of_characters_{c}"] += 1
                        data_character_distrubution["total_amount_of_characters"] += 1
                    else:
                        # New character, add it to find this list.
                        # Should escape characters be ignored
                        if ignore_escape_characters is True and (c == "\t" or c == "\n" or c == "\r"):
                            continue
                        find_this.append(c)
                        data_character_distrubution[f"occurrence_of_characters_{c}"] = 1
                        data_character_distrubution[f"percentage_of_file_that_is_{c}"] = 0
                        data_character_distrubution["total_amount_of_characters"] += 1
            # Calculate the percentage of the specific number occured, in comparison to total amount of numbers that occured
            for key in data_character_distrubution:
                end = key[-1]
                cmp = key[:-1]
                if "percentage_of_file_that_is_" == cmp:
                    data_character_distrubution[f"percentage_of_file_that_is_{end}"] = data_character_distrubution[f"occurrence_of_characters_{end}"] / \
                                                                                       data_character_distrubution["total_amount_of_characters"]
    except FileNotFoundError:
        print("ERROR!", file = sys.stderr)
        print(f"The file {filename_to_read} was not found,", file = sys.stderr)
        print(f"Calculating the distribution of numbers in the file {filename_to_read} was aborted", file = sys.stderr)
        data_character_distrubution = {}
    return data_character_distrubution
def get_distrubution_of_digits_in_file(filename_to_read):
    """Return the distribution of digits in the file to read from."""
    data_number_distrubution = {}
    find_this = []
    try:
        if os.stat(filename_to_read).st_size == 0:
            print(f"The file {filename_to_read} is empty!")
        else:
            # Initialize the dictionary and list, which hold the return value and what to search for
            for n in range(0, 10):
                data_number_distrubution[f"occurrence_of_number_{n}"] = 0
                data_number_distrubution[f"percentage_of_number_{n}"] = 0
                # what to searching for
                find_this.append(str(n))
            data_number_distrubution["total_amount_of_numbers"] = 0
            
            # Count decimal numbers
            with open(filename_to_read) as f:
                while True:
                    # Read from file
                    c = f.read(1)
                    if not c:
                        break
                    if c in find_this:
                        data_number_distrubution[f"occurrence_of_number_{c}"] += 1
                        data_number_distrubution["total_amount_of_numbers"] += 1
                    # ignore dot
                    elif c == ".":
                        pass
                    else:
                        # Found a nonnumerical character or not correctly formatted, this is a error
                        raise number_has_nonnumerical_characters_error
            # Calculate the percentage of the specific number occured, in comparison to total amount of numbers that occured
            for n in range(0, 10):
                data_number_distrubution[f"percentage_of_number_{n}"] = \
                data_number_distrubution[f"occurrence_of_number_{n}"] / data_number_distrubution["total_amount_of_numbers"]
    except number_has_nonnumerical_characters_error:
        print("ERROR!", file = sys.stderr)
        print(f"The file {filename_to_read} has nonnumerical number(s) or is not correctly formatted(e.g.:new line),", file = sys.stderr)
        print(f"Calculating the distribution of numbers in the file {filename_to_read} was aborted", file = sys.stderr)
        data_number_distrubution = {}
    except FileNotFoundError:
        print("ERROR!", file = sys.stderr)
        print(f"The file {filename_to_read} was not found,", file = sys.stderr)
        print(f"Calculating the distribution of numbers in the file {filename_to_read} was aborted", file = sys.stderr)
        data_number_distrubution = {}
    return data_number_distrubution
def get_distrubution_of_digits_in_file_base_hex(filename_to_read):
    """Return the distribution of digits in the in base-16."""
    data_number_distrubution = {}
    find_this = []
    try:
        if os.stat(filename_to_read).st_size == 0:
            print(f"The file {filename_to_read} is empty!")
        else:
            # Initialize the dictionary and list, which hold the return value and what to search for
            for n in range(0, 10):
                data_number_distrubution[f"occurrence_of_number_{n}"] = 0
                data_number_distrubution[f"percentage_of_number_{n}"] = 0
                # what to searching for
                find_this.append(str(n))
            data_number_distrubution["total_amount_of_numbers"] = 0
            
            # Count decimal numbers
            with open(filename_to_read) as f:
                while True:
                    # Read from file
                    c = f.read(1)
                    if not c:
                        break
                    if c in find_this:
                        data_number_distrubution[f"occurrence_of_number_{c}"] += 1
                        data_number_distrubution["total_amount_of_numbers"] += 1
                    # ignore dot
                    elif c == ".":
                        pass
                    else:
                        # Found a nonnumerical character or not correctly formatted, this is a error
                        raise number_has_nonnumerical_characters_error
            # Calculate the percentage of the specific number occured, in comparison to total amount of numbers that occured
            for n in range(0, 10):
                data_number_distrubution[f"percentage_of_number_{n}"] = \
                data_number_distrubution[f"occurrence_of_number_{n}"] / data_number_distrubution["total_amount_of_numbers"]
    except number_has_nonnumerical_characters_error:
        print("ERROR!", file = sys.stderr)
        print(f"The file {filename_to_read} has nonnumerical number(s) or is not correctly formatted(e.g.:new line),", file = sys.stderr)
        print(f"Calculating the distribution of numbers in the file {filename_to_read} was aborted", file = sys.stderr)
        data_number_distrubution = {}
    except FileNotFoundError:
        print("ERROR!", file = sys.stderr)
        print(f"The file {filename_to_read} was not found,", file = sys.stderr)
        print(f"Calculating the distribution of numbers in the file {filename_to_read} was aborted", file = sys.stderr)
        data_number_distrubution = {}
    return data_number_distrubution
def get_distributing_of_character_compared_to_each_other(filename):
    count_data = {}
    if os.stat(filename).st_size == 0:
        print(f"The file {filename} is empty!", file = sys.stdout)
    else:
        # Initialize what to searching for
        find_this = []
        
        # Count characters
        with open(filename) as f:
            while True:
                # Read from file
                c = f.read(1)
                if not c:
                    break
                if c in find_this:
                    count_data[c]["sum_of_value_found_distance"] += count_data[c]["n-th_last_time_character_was_found"]
                    count_data[c]["n-th_last_time_character_was_found"] = 0
                    count_data[c]["total_number_of_character_found"] += 1
                else:
                    # new character found, add it to what to find
                    find_this.append(c)
                    count_data[c] = { "n-th_last_time_character_was_found" : 0,
                                       "sum_of_value_found_distance" : 0,
                                       "total_number_of_character_found" : 1,
                                       "distribution_of_value" : 0
                                     }
                # add to all character that have been found +1, except for the character that was read
                for key, value in count_data.items():
                    if (key != c):
                        value["n-th_last_time_character_was_found"] += 1
        # calculate the percentage/fraction the value occurred, compared to total distance that value has, sumed
        for key, value in count_data.items():
            value["distribution_of_value"] = value["sum_of_value_found_distance"] / value["total_number_of_character_found"]
    return count_data

def print_distrubution_of_characters(data, filename):
    if any(data):
        print(f"File: {filename}", file = sys.stdout)
        print("Character |   %   | Number of occurrence", file = sys.stdout)
        for key, value in data.items():
            end = key[-1]
            cmp = key[:-1]
            if "percentage_of_file_that_is_" == cmp:
                p = round(data[f"percentage_of_file_that_is_{end}"], 3)
                p = str(p)
                o = data[f"occurrence_of_characters_{end}"]
                print(f" {end:<8} | {p:<5} | {o}", file = sys.stdout)
        print(f"Total number of characters that occured: {data['total_amount_of_characters']}", file = sys.stdout)
def print_distrubution_of_digits(data, file):
    if any(data):
        print(f"File: {file}", file = sys.stdout)
        print("Number |   %   | Number of occurrence", file = sys.stdout)
        for n in range(0, 10):
            p = round(data[f"percentage_of_number_{n}"], 3)
            p = str(p)
            o = data[f"occurrence_of_number_{n}"]
            print(f" {n:<5} | {p:<5} | {o}", file = sys.stdout)
        print(f"Total numbers that occured: {data['total_amount_of_numbers']}", file = sys.stdout)
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
    
    parser.add_argument("-d", metavar = "<filename>", help = "get distribution of character in the file")
    parser.add_argument("-di", metavar = "<filename>", help = "get distribution of character in the file and ignore escape character for tab and new line")
    parser.add_argument("-dd", metavar = "<filename>", help = "get distribution of numbers in the file")
    parser.add_argument("-dhex", metavar = "<filename>", help = "get distribution of numbers in base-16 in the file")
    parser.add_argument("-dist", metavar = "<filename>", help = "get distribution of character in file compared to each other(0 == no distrubution/all characters are in a clusters, 1 == even distrubution of character in file, X > 1 more distrubuted)")

    args = parser.parse_args()
    
    # Execute commands
    if args.nsqrt is not None:
        try:
            print(get_n_non_square_number(int(args.nsqrt)))
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Getting the {args.nsqrt}-th non-square number was aborted.", file = sys.stderr)
    if args.sqrt is not None:
        try:
            save_sqrt_to_file(args.sqrt[0], args.sqrt[1], args.sqrt[2])
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Writing the square root of {args.sqrt[0]} to the file {args.sqrt[1]} was aborted", file = sys.stderr)

    if args.l is not None:
        try:
            number_of_characters_in_file(args.l)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Writing the number of characters in the file {args.l} was aborted", file = sys.stderr)
    if args.dl is not None:
        try:
            number_of_decimal_numbers_in_file(args.dl)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Writing the number of decimal numbers in the file {args.dl} was aborted", file = sys.stderr)

    if args.e is not None:
        try:
            xor_file(args.e[0], args.e[1], args.e[2])
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Encrypting the file {args.e[0]} was aborted.", file = sys.stderr)
    if args.de is not None:
        try:
            xor_file(args.de[0], args.de[1], args.de[2])
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Decrypting the file {args.e[0]} was aborted.", file = sys.stderr)

    if args.d is not None:
        try:
            data_of_character_distrubution = get_distrubution_of_characters_in_file(args.d, False)
            print_distrubution_of_characters(data_of_character_distrubution, args.d)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Calculating the distribution of characters in the file {args.d} was aborted", file = sys.stderr)
    if args.di is not None:
        try:
            data_of_character_distrubution = get_distrubution_of_characters_in_file(args.di, True)
            print_distrubution_of_characters(data_of_character_distrubution, args.di)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Calculating the distribution of characters in the file {args.di} was aborted", file = sys.stderr) 
    if args.dd is not None:
        try:
            data_of_numbers = get_distrubution_of_digits_in_file(args.dd)
            print_distrubution_of_digits(data_of_numbers, args.dd)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Calculating the distribution of numbers in the file {args.dd} was aborted", file = sys.stderr)
    if args.dhex is not None:
        try:
            data_of_numbers = get_distrubution_of_digits_in_file(args.dd)
            print_distrubution_of_digits(data_of_numbers, args.dd)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Calculating the distribution of numbers in the file {args.dd} was aborted", file = sys.stderr)
    if args.dist is not None:
        try:
            data = get_distributing_of_character_compared_to_each_other(args.dist)
            print_the_distributing_of_character_compared_to_each_other(data, args.dist)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Getting the distributing of character compared to each other  in the file {args.dist} was aborted.", file = sys.stderr)

if __name__ == '__main__':
    main()
