# ui.py

# Starter code for assignment 2 in ICS 32 Programming with
# Software Libraries in Python

# Replace the following placeholders with your information.

# Luke Phimphisane
# lphimphi@uci.edu
# 72686112

from pathlib import Path
from Profile import Profile, DsuFileError, DsuProfileError
import shlex
import operate

"""
InvalidOptionError is a custom exception handler
that is raised when attempting parse an invalid
command option during admin-mode runtime.
"""


class InvalidOptionError(Exception):
    pass


"""
Splits the shell input into a list of arguments.
input - string of shell input
Returns list of arguments derived from terminal input.
"""


def split_input(input: str) -> list:

    reader = shlex.shlex(input, posix=True)
    reader.escape = ''
    reader.whitespace_split = True
    reader.commenters = ''
    reader = list(reader)
    return reader


"""
    Checks if the input is in valid form for creating
    or opening files.
    inputs - remaining arguments of the split shell input
    NOT including the command choice. Returns whether or
    not this set of arguments is generally in the valid form.
"""


def validate_inputs(arguments: list) -> bool:
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


"""
Uses shell arguments to create a .dsu path in the desired location.
inputs - remaining arguments of the split shell input NOT including
the command choice. Returns a resolved .dsu path at the desired location
with the specified name.
"""


def create_path(inputs: list) -> str:
    file_directory = Path(inputs[0])
    file_name = str(inputs[2]) + ".dsu"
    file_path = file_directory / file_name
    if not file_directory.exists():
        raise FileNotFoundError
    file_path = file_path.resolve()
    return str(file_path)


"""
Prompts the user to input their username, password, and bio to
store it into the given Profile object. Can be customized
to have a text prompt to guide the user and does not take
only-whitespace inputs as valid entries.
"""


def collect_profile_data(profile: Profile, prompt_u='',
                         prompt_p='', prompt_b='') -> None:
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


"""
Performs the necessary actions and functions in order to create
a file with a desired location and name while storing
Profile data with collected username, password, and bio.
Returns a string of the path of the created file.
"""


def handle_create(profile: Profile, inputs: list) -> str:

    valid = validate_inputs(inputs)
    if valid:
        new_path = create_path(inputs[1:])
        p = Path(new_path)
        if p.exists():
            try:
                profile._posts = []
                operate.open_file(profile, p)
                return new_path
            except AttributeError:
                print("ERROR")
            except DsuProfileError:
                print("ERROR")
            except DsuFileError:
                print("ERROR")
        try:
            collect_profile_data(profile)
            operate.create_file(new_path)
            profile.save_profile(new_path)
        except FileExistsError:
            print("ERROR")
        return new_path
    else:
        print("ERROR")


"""
Performs the file reading process using path validation
and file reading functions.

inputs - remaining arguments of the split shell input
NOT including the command choice.
"""


def handle_read(inputs: list) -> None:

    valid = validate_inputs(inputs)
    p = Path(inputs[1]).resolve()
    if valid and p.exists() and (p.suffix == '.dsu'):
        operate.read_file(p)
    else:
        print("ERROR")


"""
Performs the necessary actions and functions in order to delete
a file from shell inputs passed through as a list.
"""


def handle_delete(inputs: list) -> None:
    """
    Performs the file deletion process using path validation
    and file reading functions.
    Parameters:
    inputs - remaining arguments of the split shell input
    NOT including the command choice.
    """
    valid = validate_inputs(inputs)
    p = Path(inputs[1]).resolve()
    if valid and p.exists() and (p.suffix == '.dsu'):
        operate.delete_file(p)
    else:
        print("ERROR")


"""
Opens a file by populating the given Profile object with
the data stored in the file at the given path. First validates
the list of inputs to verify it is in correct form.
Returns the string of the path of the opened file.
"""


def handle_open(profile: Profile, inputs: list) -> str:
    valid = validate_inputs(inputs)
    if valid:
        try:
            path = inputs[1]
            profile._posts = []
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


"""
Performs the necessary actions and functions in order to print
the desired data from the given profile by stepping through the
shell input word by word and parsing through each command individually.
"""


def handle_print(profile: Profile, inputs: list) -> None:
    arguments = inputs[1:]
    accepted_options = ['-usr', '-pwd', '-bio', '-posts', '-post', '-all']
    input_required_options = ['-post']
    skip = False
    for i, argument in enumerate(arguments):
        if skip is True:
            skip = False
            continue
        if argument in input_required_options:
            operate.parse_print_options(profile, arguments[i:i+2])
            skip = True
        elif argument in accepted_options:
            operate.parse_print_options(profile, arguments[i])
        else:
            raise InvalidOptionError("ERROR")


"""
Performs the necessary actions and functions in order to edit
the desired data from the given profile by stepping through the
shell input two at a time and parsing through each command with
its option input in pairs.
"""


def handle_edit(profile: Profile, inputs: list, active_path: str) -> None:
    arguments = inputs[1:]
    accepted_options = ['-usr', '-pwd', '-bio', '-addpost', '-delpost']
    skip = False
    for i, argument in enumerate(arguments):
        if skip is True:
            skip = False
            continue
        if argument in accepted_options:
            operate.parse_edit_options(profile, arguments[i:i+2])
            profile.save_profile(active_path)
            skip = True
        else:
            raise InvalidOptionError("ERROR")


"""
Runs the corresponding function based on given commands.
Accepts "C", "D", "R", "O", "E", "P", and "Q", as valid commands.
Takes in a profile to perform work on, the arguments of the
shell command, and the path of the current file that is open.

Returns whether or not to continue and the path of the active
file.
"""


def run_command(profile: Profile, arguments: list, active_path) -> bool | str:
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
            if active_path == "":
                print("ERROR")
                return True, active_path
            try:
                handle_print(profile, arguments[:])
            except InvalidOptionError as ex:
                print(ex)
            except IndexError:
                print("ERROR")
        elif command == "E":
            if active_path == "":
                print("ERROR")
                return True, active_path
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


def run_admin(active_profile: Profile, active_path: str) -> None:
    while True:
        try:
            arguments = split_input(input())
            again, active_path = run_command(
                active_profile, arguments, active_path)
            if again:
                continue
        except (AssertionError, KeyboardInterrupt, ValueError):
            print("ERROR")
            continue
        break
