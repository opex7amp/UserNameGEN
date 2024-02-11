import random
import sys
import requests
import itertools
import threading
import time
import os
from termcolor import colored


stop_spinner = False  # don't touch this

def read_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

def generate_username(adjectives, nouns):
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f'{adjective}_{noun}'

def print_opex_banner():
    opex_banner = colored("""
░█████╗░██████╗░███████╗██╗░░██╗
██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝
██║░░██║██████╔╝█████╗░░░╚███╔╝░
██║░░██║██╔═══╝░██╔══╝░░░██╔██╗░
╚█████╔╝██║░░░░░███████╗██╔╝╚██╗
░╚════╝░╚═╝░░░░░╚══════╝╚═╝░░╚═╝
""", "cyan")
    print(opex_banner)

def print_opex_banner_with_shadow():
    shadow_color = "grey"
    shadow_offset = " " * 2

    opex_banner = colored("""
░█████╗░██████╗░███████╗██╗░░██╗
██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝
██║░░██║██████╔╝█████╗░░░╚███╔╝░
██║░░██║██╔═══╝░██╔══╝░░░██╔██╗░
╚█████╔╝██║░░░░░███████╗██╔╝╚██╗
░╚════╝░╚═╝░░░░░╚══════╝╚═╝░░╚═╝
""", "cyan")

    shadow_banner = colored(f'{shadow_offset}{opex_banner}', shadow_color)
    print(shadow_banner)

def main_menu():
    print_opex_banner_with_shadow()
    print(colored("1. Generate Usernames", "cyan"))
    print(colored("2. Exit", "cyan"))

def generate_and_print_usernames(num_usernames, adjectives, nouns, output_file):
    for i in range(1, num_usernames + 1):
        username = generate_username(adjectives, nouns)
        color = "cyan"
        print(colored(f"{i} | {username}", color))
        output_file.write(f"{i} | {username}\n")
        sys.stdout.flush()
        time.sleep(0.5)

def save_usernames_to_file(usernames, output_file):
    with open(output_file, 'w') as file:
        for username in usernames:
            file.write(f"{username}\n")

def funny_exit_message(num_usernames):
    messages = [
        "Mission accomplished! Specified usernames generated!",
        "Boom! You've got the usernames you wanted! Exiting...",
        "And that's a wrap! Specified usernames are ready!",
        "Ta-da! The usernames you asked for are ready to roll!",
        "You asked, we delivered! Specified usernames generated!",
    ]
    message = random.choice(messages)
    print()
    print(colored(message, "green"))

def spinner(duration=5, speed=0.2):
    global stop_spinner
    spinner_chars = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    start_time = time.time()
    while not stop_spinner and time.time() - start_time < duration:
        sys.stdout.write(colored(next(spinner_chars), "cyan"))
        sys.stdout.flush()
        time.sleep(speed)
        sys.stdout.write('\b\b\b')

if __name__ == "__main__":
    adjectives_file = os.environ.get("ADJECTIVES")
    nouns_file = os.environ.get("NOUNS")
    output_filename = os.environ.get("GENERATED")

    adjectives = read_words_from_file(adjectives_file)
    nouns = read_words_from_file(nouns_file)

    spinner_thread = threading.Thread(target=spinner, args=(5, 0.2))
    spinner_thread.start()

    time.sleep(2)

    stop_spinner = True
    spinner_thread.join()

    while True:
        main_menu()
        choice = input(colored("Enter the number of your choice: ", "cyan"))

        if choice == "1":
            try:
                num_usernames = int(input(colored("Enter how many usernames you want: ", "cyan")))
                print()

                with open(output_filename, 'w') as output_file:
                    generate_and_print_usernames(num_usernames, adjectives, nouns, output_file)

                print()
                funny_exit_message(num_usernames)
                sys.exit()

            except ValueError:
                print(colored("Invalid input. Please enter a valid number.", "red"))

        elif choice == "2":
            sys.exit()

        else:
            print(colored("Invalid choice. Please try again.", "red"))



