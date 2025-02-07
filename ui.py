# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Luke Phimphisane
# lphimphi@uci.edu
# 72686112

from pathlib import Path
from Profile import Profile, DsuFileError, DsuProfileError
import shlex
import operate


class InvalidOptionError(Exception):
    pass


def split_input(input: str) -> list:
    """
    Splits the shell input into a list of arguments.
    Parameters:
    input - string of shell input
    Return:
    reader - list of arguments derived from terminal input.
    """
    reader = shlex.shlex(input, posix=True)
    reader.escape = ''
    reader.whitespace_split = True
    reader.commenters = ''
    reader = list(reader)
    return reader


def validate_inputs(arguments: list) -> bool:
    """
    Checks if the input is in valid form for creating or opening files.
    Parameters:
    inputs - remaining arguments of the split shell input NOT including the command choice.
    Return:
    bool - Whether or not this set of arguments is generally in the valid form.
    """
    command = arguments[0]
    if command == 'C':
        try:
            accepted_options = ['-n']
            if arguments[2] in accepted_options and len(arguments) == 4:
                return True
        except IndexError:
            return False
    elif (command == 'O') or (command == 'R') or (command == 'D'):
        if len(arguments) == 2:
            return True
        else:
            return False


def create_path(inputs: list) -> str:
    """
    Uses shell arguments to create a .dsu path in the desired location.
    Parameters:
    inputs - remaining arguments of the split shell input NOT including the command choice.
    Return:
    file_path - a resolved .dsu path at the desired location with the specified name.
    """
    file_directory = Path(inputs[0])
    file_name = str(inputs[2]) + ".dsu"
    file_path = file_directory / file_name
    if not file_directory.exists():
        raise FileNotFoundError
    file_path = file_path.resolve()
    return str(file_path)


def collect_profile_data(profile: Profile, prompt_u='', prompt_p='', prompt_b='') -> None:
    username = input(prompt_u).strip()
    while username.strip() == '':
        print("ERROR")
        username = input(prompt_u)
    profile.username = username

    password = input(prompt_p).strip()
    while password.strip() == '':
        print("ERROR")
        username = input(prompt_p)
    profile.password = password

    bio = input(prompt_b).strip()
    while bio.strip() == '':
        print("ERROR")
        bio = input(prompt_b)
    profile.bio = bio


def handle_create(profile: Profile, inputs: list) -> str:
    """
    Performs the file creation process using path validation, path creation, and file creation functions.
    Parameters:
    inputs - remaining arguments of the split shell input NOT including the command choice.
    """
    valid = validate_inputs(inputs)
    if valid:
        new_path = create_path(inputs[1:])
        p = Path(new_path)
        if p.exists():
            operate.open_file(profile, new_path)
        else:
            try:
                collect_profile_data(profile)
                operate.create_file(new_path)
                profile.save_profile(new_path)
            except FileExistsError:
                print("ERROR")
            return new_path
    else:
        print("ERROR")


def handle_read(inputs: list):
    """
    Performs the file reading process using path validation and file reading functions.
    Parameters:
    inputs - remaining arguments of the split shell input NOT including the command choice.
    """
    valid = validate_inputs(inputs)
    p = Path(inputs[1]).resolve()
    if valid and p.exists() and (p.suffix == '.dsu'):
        operate.read_file(p)
    else:
        print("ERROR")


def handle_delete(inputs: list):
    """
    Performs the file deletion process using path validation and file reading functions.
    Parameters:
    inputs - remaining arguments of the split shell input NOT including the command choice.
    """
    valid = validate_inputs(inputs)
    p = Path(inputs[1]).resolve()
    if valid and p.exists() and (p.suffix == '.dsu'):
        operate.delete_file(p)
    else:
        print("ERROR")


def handle_open(profile: Profile, inputs: list) -> str:
    valid = validate_inputs(inputs)
    if valid:
        try:
            path = inputs[1]
            operate.open_file(profile, path)
            return path
        except AttributeError:
            print("ERROR")
        except DsuProfileError:
            print("ERROR")
        except DsuFileError:
            print("ERROR")
    else:
        print("ERROR")


def handle_print(profile: Profile, inputs: list):
    arguments = inputs[1:]
    accepted_options = ['-usr', '-pwd', '-bio', '-posts', '-post', '-all']
    input_required_options = ['-post']
    skip = False
    for i, argument in enumerate(arguments):
        if skip == True:
            skip = False
            continue
        if argument in input_required_options:
            operate.parse_print_options(profile, arguments[i:i+2])
            skip = True
        elif argument in accepted_options:
            operate.parse_print_options(profile, arguments[i])
        else:
            raise InvalidOptionError("ERROR")


def handle_edit(profile: Profile, inputs: list, active_path: str):
    arguments = inputs[1:]
    accepted_options = ['-usr', '-pwd', '-bio', '-addpost', '-delpost']
    skip = False
    for i, argument in enumerate(arguments):
        if skip == True:
            skip = False
            continue
        if argument in accepted_options:
            operate.parse_edit_options(profile, arguments[i:i+2])
            profile.save_profile(active_path)
            skip = True
        else:
            raise InvalidOptionError("ERROR")


def run_command(profile: Profile, arguments: list, active_path):
    """
    Runs the corresponding function based on given commands.
    Accepts "C", "O", "E", and "P", as valid commands.
    Parameters:
    arguments - arguments of the split shell input INCLUDING the command choice.
    """
    try:
        command = arguments[0]
        if command == "C":
            active_path = handle_create(profile, arguments[:])
        elif command == "R":
            handle_read(arguments[:])
        elif command == "O":
            active_path = handle_open(profile, arguments[:])
        elif command == "D":
            handle_delete(arguments[:])
        elif command == "P":
            try:
                handle_print(profile, arguments[:])
            except InvalidOptionError as ex:
                print(ex)
            except IndexError:
                print("ERROR")
        elif command == "E":
            try:
                handle_edit(profile, arguments[:], active_path)
            except InvalidOptionError as ex:
                print(ex)
            except IndexError:
                print("ERROR")
        elif command == "Q":
            return False, active_path
        else:
            print("ERROR")
    except (IndexError, AssertionError, ValueError, OSError):
        print("ERROR")
    return True, active_path


def run_admin(active_profile: Profile, active_path: str):

    try:
        arguments = split_input(input())
        again, new_active_path = run_command(
            active_profile, arguments, active_path)
        if again:
            run_admin(active_profile, new_active_path)
    except (AssertionError, KeyboardInterrupt, ValueError):
        print("ERROR")
        run_admin(active_profile, active_path)


OPEN_FILE_ASK = "Enter the path of the file you would like to open:"
OPEN_FILE_WRONG_INPUT = "There was an error reading your input. Try again:"
OPEN_FILE_NONEXIST = "That file does not appear to exist. Try again:"
OPEN_FILE_SUCCESS = "\nFile was successfully opened!"


def ui_open_file(profile: Profile) -> str:

    print(OPEN_FILE_ASK)
    while True:
        try:
            path_name = split_input(input())
        except (KeyboardInterrupt, ValueError):
            print(OPEN_FILE_WRONG_INPUT)
            continue
        if len(path_name) != 1:
            print(OPEN_FILE_WRONG_INPUT)
            continue
        p = Path(path_name[0])
        if not p.exists():
            print(OPEN_FILE_NONEXIST)
            continue
        operate.open_file(profile, str(p))
        break

    print(OPEN_FILE_SUCCESS)
    return str(p)


CREATE_FILE_PATH_ASK = "Now creating a file... Please enter a directory:"
CREATE_FILE_WRONG_INPUT = "There was an error reading your input. Try again:"
CREATE_FILE_DIR_NONEXIST = "That directory does not appear to exist. Try again:"
CREATE_FILE_NAME_ASK = "Directory is valid. Now enter a file name:"
CREATE_FILE_EXISTS = "File already exists. Proceeding to open file..."
CREATE_FILE_USERNAME_ASK = "Enter a username:"
CREATE_FILE_PASSWORD_ASK = "Enter a password:"
CREATE_FILE_BIO_ASK = "Enter a bio:"
CREATE_FILE_EXIST_INTERRUPT = "File was found while collecting data. Process terminated. Restarting."
CREATE_FILE_SUCCESSFUL = "\nFile was successfully created!"


def ui_create(profile: Profile) -> str:

    print(CREATE_FILE_PATH_ASK)
    while True:
        try:
            directory = split_input(input())
        except (KeyboardInterrupt, ValueError):
            print(CREATE_FILE_WRONG_INPUT)
            continue
        if len(directory) != 1:
            print(CREATE_FILE_WRONG_INPUT)
            continue
        dir = Path(directory[0])
        if not dir.exists():
            print(CREATE_FILE_DIR_NONEXIST)
            continue
        break

    print(CREATE_FILE_NAME_ASK)
    while True:
        try:
            name = split_input(input())
        except (KeyboardInterrupt, ValueError):
            print(CREATE_FILE_WRONG_INPUT)
            continue
        if len(name) != 1:
            print(CREATE_FILE_WRONG_INPUT)
            continue
        name = name[0]
        break

    path = dir / (str(name) + '.dsu')

    if path.exists():
        path(CREATE_FILE_EXISTS)
        operate.open_file(profile, str(path))
        return

    collect_profile_data(profile, CREATE_FILE_USERNAME_ASK,
                         CREATE_FILE_PASSWORD_ASK, CREATE_FILE_BIO_ASK)
    try:
        operate.create_file(path)
        profile.save_profile(path)
    except FileExistsError:
        print(CREATE_FILE_EXIST_INTERRUPT)
        ui_create(profile)

    print(CREATE_FILE_SUCCESSFUL)
    return str(path)


READ_FILE_ASK = "What file would you like to read? (q to return home)"
READ_FILE_PRINT_CONFIRM = "Here are the contents of the file:\n"
READ_FILE_ERROR = "That file does not seem to exist or may not be a DSU file. Try again or q to quit:"

def ui_read():

    print(READ_FILE_ASK)
    while True:
        path = input().strip()
        p = Path(path).resolve()
        if p.exists() and (p.suffix == '.dsu'):
            print(READ_FILE_PRINT_CONFIRM)
            operate.read_file(p)
            print()
            break
        elif path == 'q':
            break
        else:
            print(READ_FILE_ERROR)


DELETE_FILE_ASK = "What file would you like to delete? (q to return home)"
DELETE_FILE_PRINT_CONFIRM = "File deleted:"
DELETE_FILE_ERROR = "That file does not seem to exist or may not be a DSU file. Try again or q to quit:"


def ui_delete():
    print(DELETE_FILE_ASK)
    while True:
        path = input().strip()
        p = Path(path).resolve()
        if p.exists() and (p.suffix == '.dsu'):
            print(DELETE_FILE_PRINT_CONFIRM)
            operate.delete_file(p)
            print(str(p))
            break
        elif path == 'q':
            break
        else:
            print(DELETE_FILE_ERROR)


PRINT_DETAILS_MENU = """Print an option using its corresponding number:
1. Username
2. Password
3. Bio
4. All posts
5. One post [choose ID]
6. Everything
7. Return to home (q)"""
PRINT_DETAILS_WRONG_INPUT = "There was an error reading your input. Try again or q to quit:"
PRINT_DETAILS_INDEX_ERROR = "ID is invalid. Try again or q to quit:"
PRINT_DETAILS_NO_POSTS = "There are no posts to print!"
PRINT_DETAILS_INVALID_OPTION = "That is not a valid option. Try again:"


def ui_print(profile:Profile) -> None:
    print(PRINT_DETAILS_MENU)
    while True:
        option = input().strip()
        if option == '1':
            print(f"Username: {profile.username}")
            break
        elif option == '2':
            print(f"Password: {profile.password}")
            break
        elif option == '3':
            print(f"Bio: {profile.bio}")
            break
        elif option == '4':

            if not profile.get_posts():
                print(PRINT_DETAILS_NO_POSTS)
                break

            print("All posts:")
            for i, post in enumerate(profile.get_posts()):
                print(f'  ID {i}: {post._entry}')

            break
            
        elif option == '5':

            if not profile.get_posts():
                print(PRINT_DETAILS_NO_POSTS)
                break

            while True:
                try:
                    id = int(input().strip())
                    print(f"Here is note: {profile.get_posts()[id].get_entry()}")
                    break
                except ValueError:
                    print(PRINT_DETAILS_WRONG_INPUT)
                except IndexError:
                    print(PRINT_DETAILS_INDEX_ERROR)
            break

        elif option == '6':
            print(f"Username: {profile.username}")
            print(f"Password: {profile.password}")
            print(f"Bio: {profile.bio}")

            if not profile.get_posts():
                print(PRINT_DETAILS_NO_POSTS)
                break

            print("All posts:")
            for i, post in enumerate(profile.get_posts()):
                print(f'  ID {i}: {post.get_entry()}')

            break
        else:
            print(PRINT_DETAILS_INVALID_OPTION)




def ui_stage_1(profile: Profile, option: str) -> str:
    if option == 'O':
        active_path = ui_open_file(profile)
    elif option == 'C':
        active_path = ui_create(profile)

    return active_path


COMMAND_OPTIONS_MENU = """====================
Welcome to your Journal!
Select an option using its corresponding number:
1. Create a file
2. Open a file
3. Read a file
4. Delete a file
5. Print details from a file
6. Edit details from a file
7. Quit (q)
====================
"""


def print_menu():
    print(COMMAND_OPTIONS_MENU)


def ui_stage_2(profile: Profile, path: str) -> str:

    active_path = path
    print_menu()

    option = input().strip()
    if option == '1':
        active_path = ui_create(profile)
    elif option == '2':
        active_path = ui_open_file(profile)
    elif option == '3':
        ui_read()
    elif option == '4':
        ui_delete()
    elif option == '5':
        ui_print(profile)
    elif option in ['7', 'q']:
        return
    
    ui_stage_2(profile, active_path)



def run_standard(active_profile: Profile, option: str):
    active_path = ui_stage_1(active_profile, option)
    ui_stage_2(active_profile, active_path)