# a1.py

# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Luke Phimphisane
# lphimphi@uci.edu
# 72686112

from Profile import Profile
import ui

WELCOME_MESSAGE = "Welcome to your python Journal!"
START_PROMPT = "Would you like to start by opening a DSU file or creating one? (O or C):"
INVALID_COMMAND_MSG = "Sorry, that is an invalid command. Please try again (O or C):"


def startup():
    current_profile = Profile()
    default_path = ''
    invalid = True

    print(WELCOME_MESSAGE)
    print(START_PROMPT)

    while invalid:
        option = input()
        if option == 'admin':
            invalid = False
            run_admin(current_profile, default_path)
        elif (option == 'O') or (option == 'C'):
            invalid = False
            ui.run_standard(current_profile, default_path, option)
        else:
            print(INVALID_COMMAND_MSG)


def run_admin(active_profile: Profile, active_path: str):

    try:
        arguments = ui.split_input(input())
        again, new_active_path = ui.run_command(
            active_profile, arguments, active_path)
        if again:
            run_admin(active_profile, new_active_path)
    except (AssertionError, KeyboardInterrupt, ValueError):
        print("Error")
        run_admin(active_profile, active_path)


if __name__ == "__main__":
    startup()
