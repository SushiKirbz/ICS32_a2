# a1.py

# Starter code for assignment 1 in ICS 32 Programming with
# Software Libraries in Python

# Replace the following placeholders with your information.

# Luke Phimphisane
# lphimphi@uci.edu
# 72686112

from Profile import Profile
import ui
import ui_friendly

WELCOME_MESSAGE = "Welcome to your python Journal!"
START_PROMPT = ("Would you like to start by opening a DSU file"
                " or creating one? (O or C):")
INVALID_COMMAND_MSG = ("Sorry, that is an invalid command."
                       " Please try again (O or C):")


def print_welcome():
    print(WELCOME_MESSAGE)
    print(START_PROMPT)


def main():
    current_profile = Profile()
    default_path = ''
    invalid = True
    print_welcome()
    while invalid:
        option = input().strip()
        if option == 'admin':
            invalid = False
            ui.run_admin(current_profile, default_path)
        elif (option == 'O') or (option == 'C'):
            invalid = False
            ui_friendly.run_standard(current_profile, option)
        else:
            print(INVALID_COMMAND_MSG)


if __name__ == "__main__":
    main()
