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

class negative_number_error(Exception):
    """The number is negative."""
    def __init__(self, msg = "Unknown error"):
        # Call the base class constructor
        super().__init__(msg)
            
        # save custom message
        self.msg = msg
    def __str__(self):
        return(self.msg)

def save_sqrt_to_file(radicand, write_to_filename, number_of_precision):
    """Save root of the radican squared in the file to write to."""
    try:
        # check that the number to square root is correct format
        error_counter = 0
        radicand = int(radicand)
        if radicand < 0:
            raise negative_number_error("The number to square root is negative,")
        # check the value to square root precision to
        error_counter += 1
        number_of_precision = int(number_of_precision)
        if number_of_precision < 0:
            raise negative_number_error("The number to get precision of square root is negative,")
        
        # Calculate the root of the radicand
        # Set the precision
        getcontext().prec = number_of_precision
        # Square root the radicand
        root_number = Decimal(radicand).sqrt()
        # convert to string
        root_number = str(root_number)
        # write to file
        with open(write_to_filename, 'w') as file_write:
            print(root_number, file = file_write, end = '')
    except ValueError:
        print("ERROR!", file = sys.stderr)
        # Not pretty, but does work
        if error_counter == 0:
            print("The radicand to square root had nonnumerical characters,", file = sys.stderr)
        elif error_counter == 1:
            print(f"The precision value when writing the square root of the value {radicand}, had nonnumerical characters,",
                  file = sys.stderr)
        print(f"writing the square root of {radicand} to the file {write_to_filename} was aborted", file = sys.stderr)
    except negative_number_error as ex:
        print("ERROR!", file = sys.stderr)
        print(ex, file = sys.stderr)
        print(f"writing the square root of {radicand} to the file {write_to_filename} was aborted", file = sys.stderr)
    except OSError:
        print("ERROR!", file = sys.stderr)
        print(f"Could not write to the file: {write_to_filename},", file = sys.stderr)
        print(f"writing the square root of {radicand} to the file {write_to_filename} was aborted", file = sys.stderr)

#https://everydaycalculation.com/square-root-calculator.php
#
# Function under construction!
#
def sqrt_by_long_division(n):
    """
    Find square root using long division method
    """
    
    number_in_pairs_of_two = []
    
    # 1st divid the number into 2 part segments
    n = str(n)
    n = n.split(".")
    if len(n) > 2:
        pass # input error!
    quotient = n[0]
    remainder = n[1]
    
    # if quotient is odd, add 0 to the 1st, when adding in 2 pairs
    if (len(quotient) % 2) != 0:
        # number is odd
        # insert 1st number, with added 0 at the beginning
        number_in_pairs_of_two.append("0" + quotient[0])
        # remove 1st number
        quotient = quotient[1:]
    # add all numbers from quotient in 2 pairs
    i = 0
    while i < len(quotient):
        number_in_pairs_of_two.append(quotient[i:i+2])
        i += 2
    
    # now do the same with the remainder
    i = 0
    while i < len(remainder) - 1: # -1, if odd, do not add last number in this loop
        number_in_pairs_of_two.append(remainder[i:i+2])
        i += 2
    if (len(remainder) % 2) != 0:
        # number is odd
        # insert last number, with added 0 at the end
        number_in_pairs_of_two.append(remainder[-1] + "0")
        
    # 2nd perform division
    
    print(number_in_pairs_of_two, file = sys.stdout)
#x = 512.5
#sqrt_by_long_division(x)
#print(sqrt_by_long_division(x), file = sys.stdout)

def number_of_decimal_numbers_in_file(filename_to_read):
    """Return the number of decimal numbers in the file."""
    # Assign default value
    return_value = 0
    try:
        find_this = []
        
        # Initialize what to search for
        for n in range(0, 10):
            find_this.append(str(n))
            
        # Count decimal numbers
        with open(filename_to_read) as f:
            while True:
                # Read from file
                c = f.read(1)
                if not c:
                    break
                if c in find_this:
                    return_value += 1
    except FileNotFoundError:
        print("ERROR!", file = sys.stderr)
        print(f"Could not find the file {filename_to_read},", file = sys.stderr)
        print(f"Writing the number of characters in the file {filename_to_read} was aborted", file = sys.stderr)
        return_value = -1
    return return_value
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
def print_distrubution_of_digits(data, file):
    if any(data):
        print(f"File: {file}", file = sys.stdout)
        print("Number |   %   | Number of occurrence", file = sys.stdout)
        for n in range(0, 10):
            p = round(data[f"percentage_of_number_{n}"], 3)
            p = str(p)
            if len(p) == 3:
                p += "  "
            elif len(p) == 4:
                p += " "
            o = data[f"occurrence_of_number_{n}"]
            print(f" {n}     | {p} | {o}", file = sys.stdout)
        print(f"Total numbers that occured: {data['total_amount_of_numbers']}", file = sys.stdout)

def number_of_characters_in_file(filename_to_read):
    """Return the number of characters in the file."""
    # Assign default value
    return_value = -1
    try:
        with open(filename_to_read, 'r') as file:
            filename = file.read()
            len_chars = len(filename)
            return_value = len_chars
    except FileNotFoundError:
        print("ERROR!", file = sys.stderr)
        print(f"Could not find the file {filename_to_read},", file = sys.stderr)
        print(f"Writing the number of characters in the file {filename_to_read} was aborted", file = sys.stderr)
    return return_value
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
                if len(p) == 3:
                    p += "  "
                elif len(p) == 4:
                    p += " "
                o = data[f"occurrence_of_characters_{end}"]
                print(f" {end}        | {p} | {o}", file = sys.stdout)
        print(f"Total number of characters that occured: {data['total_amount_of_characters']}", file = sys.stdout)

def number_to_my_character_encoding(number):
    my_character_encoding = { "0" : " ",
              "1" : "!",
              "2" : '"',
              "3" : "#",
              "4" : "$",
              "5" : "%",
              "6" : "&",
              "7" : "'",
              "8" : "(",
              "9" : ")",
              "10" : "*",
              "11" : "+",
              "12" : ",",
              "13" : "-",
              "14" : ".",
              "15" : "/",
              "16" : "0",
              "17" : "1",
              "18" : "2",
              "19" : "3",
              "20" : "4",
              "21" : "5",
              "22" : "6",
              "23" : "7",
              "24" : "8",
              "25" : "9",
              "26" : ":",
              "27" : ";",
              "28" : "<",
              "29" : "=",
              "30" : ">",
              "31" : "?",
              "32" : "@",
              "33" : "A",
              "34" : "B",
              "35" : "C",
              "36" : "D",
              "37" : "E",
              "38" : "F",
              "39" : "G",
              "40" : "H",
              "41" : "I",
              "42" : "J",
              "43" : "K",
              "44" : "L",
              "45" : "M",
              "46" : "N",
              "47" : "O",
              "48" : "P",
              "49" : "Q",
              "50" : "R",
              "51" : "S",
              "52" : "T",
              "53" : "U",
              "54" : "V",
              "55" : "W",
              "56" : "X",
              "57" : "Y",
              "58" : "Z",
              "59" : "[",
              "60" : "\\",
              "61" : "]",
              "62" : "^",
              "63" : "_"#,
              # "64" : "`",
              # "65" : "a",
              # "66" : "b",
              # "67" : "c",
              # "68" : "d",
              # "69" : "e",
              # "70" : "f",
              # "71" : "g",
              # "72" : "h",
              # "73" : "i",
              # "74" : "j",
              # "75" : "k",
              # "76" : "l",
              # "77" : "m",
              # "78" : "n",
              # "79" : "o",
              # "80" : "p",
              # "81" : "q",
              # "82" : "r",
              # "83" : "s",
              # "84" : "t",
              # "85" : "u",
              # "86" : "v",
              # "87" : "w",
              # "88" : "x",
              # "89" : "y",
              # "90" : "z",
              # "91" : "{",
              # "92" : "|",
              # "93" : "}",
              # "94" : "~",
              # "95" : "ä",
              # "96" : "ö",
              # "97" : "å",
              # "98" : "Ä",
              # "99" : "Å"
              }
    c = my_character_encoding[str(number)]
    return c
def my_character_encoding_to_number(character):
    my_character_encoding = { " " : "00",
              "!" : "01",
              '"' : "02",
              "#" : "03",
              "$" : "04",
              "%" : "05",
              "&" : "06",
              "'" : "07",
              "(" : "08",
              ")" : "09",
              "*" : "10",
              "+" : "11",
              "," : "12",
              "-" : "13",
              "." : "14",
              "/" : "15",
              "0" : "16",
              "1" : "17",
              "2" : "18",
              "3" : "19",
              "4" : "20",
              "5" : "21",
              "6" : "22",
              "7" : "23",
              "8" : "24",
              "9" : "25",
              ":" : "26",
              ";" : "27",
              "<" : "28",
              "=" : "29",
              ">" : "30",
              "?" : "31",
              "@" : "32",
              "A" : "33",
              "B" : "34",
              "C" : "35",
              "D" : "36",
              "E" : "37",
              "F" : "38",
              "G" : "39",
              "H" : "40",
              "I" : "41",
              "J" : "42",
              "K" : "43",
              "L" : "44",
              "M" : "45",
              "N" : "46",
              "O" : "47",
              "P" : "48",
              "Q" : "49",
              "R" : "50",
              "S" : "51",
              "T" : "52",
              "U" : "53",
              "V" : "54",
              "W" : "55",
              "X" : "56",
              "Y" : "57",
              "Z" : "58",
              "[" : "59",
              "\\" : "60",
              "]" : "61",
              "^" : "62",
              "_" : "63"#,
              # "`" : "64",
              # "a" : "65",
              # "b" : "66",
              # "c" : "67",
              # "d" : "68",
              # "e" : "69",
              # "f" : "70",
              # "g" : "71",
              # "h" : "72",
              # "i" : "73",
              # "j" : "74",
              # "k" : "75",
              # "l" : "76",
              # "m" : "77",
              # "n" : "78",
              # "o" : "79",
              # "p" : "80",
              # "q" : "81",
              # "r" : "82",
              # "s" : "83",
              # "t" : "84",
              # "u" : "85",
              # "v" : "86",
              # "w" : "87",
              # "x" : "88",
              # "y" : "89",
              # "z" : "90",
              # "{" : "91",
              # "|" : "92",
              # "}" : "93",
              # "~" : "94",
              # "ä" : "95",
              # "ö" : "96",
              # "å" : "97",
              # "Ä" : "98",
              # "Å" : "99"
              }
    return int(my_character_encoding[character])

def xor_encrypt(character, two_decimal_digits):
    print(character, file = sys.stderr)
    chipercharacter = my_character_encoding_to_number(character)
    key = int(two_decimal_digits)
    while key > 63:
        key -= 63
        
    # xor
    chiper = chipercharacter ^ key
    
    #print(chiper)
    # return character
    return number_to_my_character_encoding(chiper)
    #ord
    #chr
def xor_decrypt(character, three_decimal_digits):
    chipercharacter = my_character_encoding_to_number(character)
    key = int(three_decimal_digits)
    while key > 63:
        key -= 63
        
    # xor
    plain_text_number = chipercharacter ^ key
    
    # return character
    return number_to_my_character_encoding(plain_text_number)

def encrypt_file(plain_text_file, key_file, file_to_store_chiper):
    if os.stat(plain_text_file).st_size == 0:
        print(f"The file {plain_text_file} is empty!", file = sys.stdout)
    else:
        if os.stat(key_file).st_size == 0:
            print(f"The file {key_file} is empty!", file = sys.stdout)
        else:
            # Initialize what to searching for
            find_this = []
            for n in range(0, 10):
                find_this.append(str(n))
            
            key_text_not_enough_data = False
            with open(plain_text_file) as plain_text, open(key_file) as key_text, open(file_to_store_chiper, 'w') as chiper_text:
                while True:
                    character_to_encrypt = plain_text.read(1)
                    if not character_to_encrypt:
                        break
                    key = ""
                    # Get 3 character from the key text, as key for the encryption
                    while len(key) < 2:
                        c = key_text.read(1)
                        if not c:
                            key_text_not_enough_data = True
                            break
                        if c in find_this:
                            key += c
                    # end loop if there dose not exist enough key data
                    if key_text_not_enough_data is True:
                        break
                    #print("C: " + character_to_encrypt + " k:" + key, file = sys.stderr)
                    # get chiper and write chiper to file
                    encrypted_character = xor_encrypt(character_to_encrypt, key)
                    #print("E: " + encrypted_character, file = sys.stderr)
                    chiper_text.write(encrypted_character)
    
def decrypt_file(chiper_file, key_file, file_to_store_plain_text):
    if os.stat(chiper_file).st_size == 0:
        print(f"The file {chiper_file} is empty!", file = sys.stdout)
    else:
        if os.stat(key_file).st_size == 0:
            print(f"The file {key_file} is empty!", file = sys.stdout)
        else:
            # Initialize what to searching for
            find_this = []
            for n in range(0, 10):
                find_this.append(str(n))
            
            key_text_not_enough_data = False
            with open(chiper_file) as plain_text, open(key_file) as key_text, open(file_to_store_plain_text, 'w') as plain_text_write:
                while True:
                    character_to_decrypt = plain_text.read(1)
                    if not character_to_decrypt:
                        break
                    key = ""
                    # Get 3 character from the key text, as key for the encryption
                    while len(key) < 2:
                        c = key_text.read(1)
                        if not c:
                            key_text_not_enough_data = True
                            break
                        if c in find_this:
                            key += c
                    # end loop if there dose not exist enough key data
                    if key_text_not_enough_data is True:
                        break
                    #print("C: " + character_to_decrypt + " k:" + key, file = sys.stderr)
                    # get chiper and write chiper to file
                    encrypted_character = xor_decrypt(character_to_decrypt, key)
                    #print("E: " + encrypted_character, file = sys.stderr)
                    plain_text_write.write(encrypted_character)


def get_n_non_square_number(n):
    """Get the Nth non square number"""
    # Proof: https://www.jstor.org/stable/3618253?seq=1
    return n + math.floor(0.5 + math.sqrt(n))

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
def print_the_distributing_of_character_compared_to_each_other(data, filename):
    if any(data):
        print(f"File: {filename}", file = sys.stdout)
        print(" character | distribution of value | sum of value found distance | total number of character found", file = sys.stdout)
        for key, value in data.items():
            dv = round(value["distribution_of_value"], 5)
            dv = str(dv)
            l = len(dv)
            l = 22 - l # len ("distribution of value ") = 22
            while l > 1:
                dv += " "
                l -= 1
            svd = str(value["sum_of_value_found_distance"])
            l = len(svd)
            l = 28 - l # len ("sum of value found distance ") = 28
            while l > 1:
                svd += " "
                l -= 1
            tnf = str(value["total_number_of_character_found"])
            print(f" {key}         | {dv} | {svd} | {tnf}", file = sys.stdout)

def main():
    parser = argparse.ArgumentParser(description = "Irrational number cipher")
    parser.add_argument("-sqrt", nargs = 3, metavar = ("<number to sqrt>",
                        "<file name to store file in>", "<precision to calculate to>"),
                        help = "generate text file with square root to the number of precision specified")
    parser.add_argument("-d", metavar = "<filename>", help = "get distribution of character in the file")
    parser.add_argument("-di", metavar = "<filename>", help = "get distribution of character in the file and ignore escape character for tab and new line")
    parser.add_argument("-l", metavar = "<filename>", help = "get length of file")
    parser.add_argument("-dd", metavar = "<filename>", help = "get distribution of numbers in the file")
    parser.add_argument("-dl", metavar = "<filename>", help = "get length of file in numbers")
    parser.add_argument("-e", metavar = ("<filename to encrypt>", "<filename of file with number>", "<output filename>"), nargs = 3, help = "encrypt file")
    parser.add_argument("-de", metavar = ("<filename to deencrypt>", "<filename of file with number>", "<output filename>"), nargs = 3, help = "deencrypt file")
    parser.add_argument("-nsqrt", metavar = "<n number of square root to return>", help = "get the n-th number of non-square")
    parser.add_argument("-dist", metavar = "<filename>", help = "get distribution of character in file compared to each other(0 == no distrubution/all characters are in a clusters, 1 == even distrubution of character in file, X > 1 more distrubuted)")
    args = parser.parse_args()
    
    # Execute commands
    if args.sqrt is not None:
        try:
            save_sqrt_to_file(args.sqrt[0], args.sqrt[1], args.sqrt[2])
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"writing the square root of {args.sqrt[0]} to the file {args.sqrt[1]} was aborted", file = sys.stderr)
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
    if args.l is not None:
        try:
            number_of_characters = number_of_characters_in_file(args.l)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Writing the number of characters in the file {args.l} was aborted", file = sys.stderr)
        else:
            print(f"The length of the file {args.l} is {number_of_characters}", file = sys.stdout)
    if args.dd is not None:
        try:
            data_of_numbers = get_distrubution_of_digits_in_file(args.dd)
            print_distrubution_of_digits(data_of_numbers, args.dd)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Calculating the distribution of numbers in the file {args.dd} was aborted", file = sys.stderr)
    if args.dl is not None:
        try:
            number_of_decimal_numbers = number_of_decimal_numbers_in_file(args.dl)
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Writing the number of decimal numbers in the file {args.dl} was aborted", file = sys.stderr)
        else:
            print(f"The length of decimal numbers in the file {args.dl} is {number_of_decimal_numbers}", file = sys.stdout)
    if args.e is not None:
        try:
            encrypt_file(args.e[0], args.e[1], args.e[2])
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Encrypting the file {args.e[0]} was aborted.", file = sys.stderr)
    if args.de is not None:
        try:
            decrypt_file(args.de[0], args.de[1], args.de[2])
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Decrypting the file {args.e[0]} was aborted.", file = sys.stderr)
    if args.nsqrt is not None:
        try:
            print(get_n_non_square_number(int(args.nsqrt)))
        except Exception as e:
            print("ERROR!", file = sys.stderr)
            print(f"Unexpected error has occurred, info: {sys.exc_info()[0].__name__},", file = sys.stderr)
            print(f"Getting the {args.nsqrt}-th non-square number was aborted.", file = sys.stderr)
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
