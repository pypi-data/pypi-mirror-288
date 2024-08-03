import random
import string

def generate_password(length=12, include_upper=True, include_lower=True, include_digits=True, include_symbols=True):
    """
    Generate a random password based on user preferences.

    Args:
        length (int): Length of the password. Default is 12.
        include_upper (bool): Whether to include uppercase letters. Default is True.
        include_lower (bool): Whether to include lowercase letters. Default is True.
        include_digits (bool): Whether to include digits. Default is True.
        include_symbols (bool): Whether to include symbols. Default is True.

    Returns:
        str: The generated password.
    """
    characters = ""
    if include_upper:
        characters += string.ascii_uppercase
    if include_lower:
        characters += string.ascii_lowercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type must be selected")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def print_password(length=12, include_upper=True, include_lower=True, include_digits=True, include_symbols=True):
    password = generate_password(length, include_upper, include_lower, include_digits, include_symbols)
    print(f'Generated Password: {password}')

def prompt_user_for_password():
    try:
        length = int(input("Enter the desired password length: "))
        include_upper = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
        include_lower = input("Include lowercase letters? (y/n): ").strip().lower() == 'y'
        include_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
        include_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'
        print_password(length, include_upper, include_lower, include_digits, include_symbols)
    except ValueError:
        print("Invalid input. Please enter a valid number for the password length.")
