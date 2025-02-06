# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Luke Phimphisane
# lphimphi@uci.edu
# 72686112

from pathlib import Path
from Profile import Post, Profile, DsuFileError, DsuProfileError
import shlex


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
    elif command == 'O':
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

# move to a2.py


def create_file(path: str):
    """
    Creates a file at the given path.
    Parameters:
    path - a Path object of the desired location for file creation.
    """
    file_path = Path(path)
    file_path.touch(exist_ok=False)
    print(file_path.resolve())


def collect_profile_data(profile: Profile) -> None:
    profile.username = input()
    profile.password = input()
    profile.bio = input()


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
            open_file(profile, new_path)
        else:
            try:
                collect_profile_data(profile)
                create_file(new_path)
                profile.save_profile(new_path)
            except FileExistsError:
                print("Error, file was created before collection process was finished.")
                print("Collected data will be discarded.")
            return new_path
    else:
        print("Error, the command is not in a valid format for creating files")


def open_file(profile: Profile, path: str):
    try:
        profile.load_profile(path)
    except DsuProfileError:
        print("This file is having issues with the Profile format")
    except DsuFileError:
        print("The file does not seem to exist or is of an invalid file type")
    else:
        print("Profile successfully loaded")


def handle_open_file(profile: Profile, inputs: list) -> str:
    valid = validate_inputs(inputs)
    if valid:
        try:
            path = inputs[1]
            open_file(profile, path)
            return path
        except AttributeError:
            print("This file does not support the Journal Profile format.")
    else:
        print("Error, the command is not in a valid format")


def parse_print_options(profile: Profile, input):
    if type(input) == str:
        option = input
    else:
        option = input[0]
        argument = input[1]
    if option == '-usr':
        print(f"Username: {profile.username}")
    elif option == '-pwd':
        print(f"Password: {profile.password}")
    elif option == '-bio':
        print(f"Bio: {profile.bio}")
    elif option == '-posts':
        print("All posts:")
        for i, post in enumerate(profile.get_posts()):
            print(f'ID {i}: {post._entry}')
    elif option == '-post':
        try:
            print(profile.get_posts()[int(argument)].get_entry())
        except ValueError:
            print(f"{argument} is not a number.")
        except IndexError:
            print("Error, not a valid ID")
    elif option == '-all':
        print(f"Username: {profile.username}")
        print(f"Password: {profile.password}")
        print(f"Bio: {profile.bio}")
        print("All posts:")
        for i, post in enumerate(profile.get_posts()):
            print(f'  ID {i}: {post.get_entry()}')
    else:
        print(f"failed to print, no options matched: option = {option}")


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
            parse_print_options(profile, arguments[i:i+2])
            skip = True
        elif argument in accepted_options:
            parse_print_options(profile, arguments[i])
        else:
            raise InvalidOptionError(
                f"Error, \"{argument}\" is not a valid option")


def parse_edit_options(profile: Profile, input: list):

    option = input[0]
    argument = input[1]

    if option == '-usr':
        profile.username = argument
        print(f"Username changed to: {profile.username}")
    elif option == '-pwd':
        profile.password = argument
        print(f"Password changed to: {profile.password}")
    elif option == '-bio':
        profile.bio = argument
        print(f"Bio changed to: {profile.bio}")
    elif option == '-addpost':
        new_post = Post()
        new_post.entry = argument
        profile.add_post(new_post)
        print(f"Added post: {argument}")
    elif option == '-delpost':
        posts = profile.get_posts()[:]
        success = profile.del_post(int(argument))
        if success:
            print(f"\tDeleted post ID {int(argument)}: {
                  posts[int(argument)].get_entry()}")
        else:
            print("Error, invalid post ID")

    else:
        print(f"failed to print, no options matched: option = {option}")


def handle_edit(profile: Profile, inputs: list, active_path: str):
    arguments = inputs[1:]
    accepted_options = ['-usr', '-pwd', '-bio', '-addpost', '-delpost']
    skip = False
    for i, argument in enumerate(arguments):
        if skip == True:
            skip = False
            continue
        if argument in accepted_options:
            parse_edit_options(profile, arguments[i:i+2])
            profile.save_profile(active_path)
            skip = True
        else:
            raise InvalidOptionError(
                f"Error, \"{argument}\" is not a valid option")


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
        elif command == "O":
            active_path = handle_open_file(profile, arguments[:])
        elif command == "Q":
            return False, active_path
        elif command == "P":
            try:
                handle_print(profile, arguments[:])
            except InvalidOptionError as ex:
                print(ex)
            except IndexError:
                print("Failed to provide an input to an option")
        elif command == "E":
            try:
                handle_edit(profile, arguments[:], active_path)
            except InvalidOptionError as ex:
                print(ex)
            except IndexError:
                print("Failed to provide an input to an option")
        else:
            print("Not a valid command")
    except (IndexError, AssertionError, ValueError):
        print("Error, invalid command or malformed key input")
    except (OSError):
        print("Error with operating system or program permissions")
    return True, active_path


def run_standard(active_profile: Profile, active_path: str, option: str):
    pass
