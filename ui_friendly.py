# Luke Phimphisane
# lphimphi@uci.edu
# 72686112

import ui
import operate
from Profile import Profile, Post, DsuFileError, DsuProfileError
from pathlib import Path

"""
Each option has its own function to support a more
user-friendly interface. Print messages are separated
to the top of each function to make editing and reading easier.
"""

OPEN_FILE_ASK = "Enter the path of the file you would like to open:"
OPEN_FILE_WRONG_INPUT = "There was an error reading your input. Try again:"
OPEN_FILE_NONEXIST = "That file does not appear to exist. Try again:"
OPEN_FILE_SUCCESS = "\nFile was successfully opened!"
OPEN_FILE_DSUFILEERROR = "This file does not support the Profile format"
OPEN_FILE_DSUPROFILEERROR = "The file doesn't exist or is not a DSU"
OPEN_FILE_UNEXPECTED_ERROR = "There was an unexpected error!"

"""
Guides the user through the file opening process.

Asks for a DSU file to open and then populates the
given profile with the information stored in the
file if possible.
"""


def ui_open_file(profile: Profile) -> str:

    print(OPEN_FILE_ASK)
    while True:
        try:
            path_name = ui.split_input(input())
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
        try:
            profile._posts = []
            operate.open_file(profile, str(p))
        except DsuProfileError:
            print(OPEN_FILE_DSUPROFILEERROR)
            continue
        except DsuFileError:
            print(OPEN_FILE_DSUFILEERROR)
            continue
        except Exception:
            print(OPEN_FILE_UNEXPECTED_ERROR)
            continue
        break

    print(OPEN_FILE_SUCCESS)
    return str(p)


CREATE_FILE_PATH_ASK = "Now creating a file... Please enter a directory:"
CREATE_FILE_WRONG_INPUT = "There was an error reading your input. Try again:"
CREATE_FILE_DIR_NONEXIST = ("That directory does not appear to exist."
                            " Try again:")
CREATE_FILE_NAME_ASK = "Directory is valid. Now enter a file name:"
CREATE_FILE_EXISTS = "File already exists. Proceeding to open file..."
CREATE_FILE_DSUFILEERROR = "This file does not support the Profile format"
CREATE_FILE_DSUPROFILEERROR = "The file doesn't exist or is not a DSU"
CREATE_FILE_UNEXPECTED_ERROR = "There was an unexpected error!"
CREATE_FILE_USERNAME_ASK = "Enter a username:"
CREATE_FILE_PASSWORD_ASK = "Enter a password:"
CREATE_FILE_BIO_ASK = "Enter a bio:"
CREATE_FILE_EXIST_INTERRUPT = ("File was found while collecting data."
                               " Process terminated. Restarting.")
CREATE_FILE_SUCCESSFUL = "\nFile was successfully created!"

"""
Guides the user through the file creation process.

First asks for a directory and file name to create--
if the file already exists, it is opened instead,
if not, a username, password, and bio is requested.

The file is created at the path as the function finishes.
"""


def ui_create(profile: Profile) -> str:

    print(CREATE_FILE_PATH_ASK)
    while True:
        try:
            directory = ui.split_input(input())
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
            name = ui.split_input(input())
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
        print(CREATE_FILE_EXISTS)
        try:
            profile._posts = []
            operate.open_file(profile, str(path))
        except DsuProfileError:
            print(CREATE_FILE_DSUPROFILEERROR)
        except DsuFileError:
            print(CREATE_FILE_DSUFILEERROR)
        except Exception:
            print(CREATE_FILE_UNEXPECTED_ERROR)
        return str(path)

    ui.collect_profile_data(profile, CREATE_FILE_USERNAME_ASK,
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
READ_FILE_ERROR = ("That file does not seem to exist or may not be a DSU file."
                   " Try again or q to quit:")

"""
Asks the reader to provide a file path to read
the contents of. Reading files does not inform
the user if it is empty or not.
"""


def ui_read() -> None:

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
DELETE_FILE_ERROR = ("That file does not seem to exist or may not be a DSU"
                     " file. Try again or q to quit:")

"""
Asks the reader to provide a file path to delete.
If the file the user wants to delete is invalid,
they will keep being prompted until a valid file
is given or the user quits the process.
"""


def ui_delete() -> None:
    print(DELETE_FILE_ASK)
    while True:
        path = input().strip()
        p = Path(path).resolve()
        if p.exists() and (p.suffix == '.dsu'):
            print(DELETE_FILE_PRINT_CONFIRM)
            operate.delete_file(p)
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
PRINT_DETAILS_WRONG_INPUT = ("There was an error reading your input."
                             " Try again or q to quit:")
PRINT_DETAILS_ASK_ID = "Enter the ID of the note you want to print:"
PRINT_DETAILS_INDEX_ERROR = "ID is invalid. Try again or q to quit:"
PRINT_DETAILS_NO_POSTS = "There are no posts to print!"
PRINT_DETAILS_INVALID_OPTION = "That is not a valid option. Try again:"

"""
Guides the user through printing details from
a Profile object. The system will print a menu
to provide the user with available options, printing
the corresponding data from the passed Profile object.
"""


def ui_print(profile: Profile) -> None:
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
                    print(PRINT_DETAILS_ASK_ID)
                    id = int(input().strip())
                    print(f"Here is the note: {
                          profile.get_posts()[id].get_entry()}")
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
        elif option in ['7', 'q']:
            break
        else:
            print(PRINT_DETAILS_INVALID_OPTION)


EDIT_DETAILS_MENU = """Edit an option using its corresponding number:
1. Username
2. Password
3. Bio
4. Add a post
5. Delete a post
6. Return to home (q)"""
EDIT_DETAILS_WRONG_INPUT = ("There was an error reading your input."
                            " Try again or q to quit:")
EDIT_DETAILS_ASK_USERNAME = "Enter a new username:"
EDIT_DETAILS_ASK_PASSWORD = "Enter a new password:"
EDIT_DETAILS_ASK_BIO = "Enter a new bio:"
EDIT_DETAILS_ASK_ADD_POST = "Type a post to add:"
EDIT_DETAILS_ASK_DEL_POST = "Enter the ID of the note you want to delete:"
EDIT_DETAILS_INDEX_ERROR = "ID is invalid. Try again or q to quit:"
EDIT_DETAILS_INVALID_OPTION = "That is not a valid option. Try again:"

"""
Guides the user through editing details from
a Profile object. The system will print a menu
to provide the user with available options, prompting
them a second time once an option is chosen and
new data is needed to change the Profile object.

Profile data is saved to the file path at the
end of running.
"""


def ui_edit(profile: Profile, path: str) -> None:
    print(EDIT_DETAILS_MENU)
    while True:
        option = input().strip()
        if option == '1':
            print(EDIT_DETAILS_ASK_USERNAME)
            profile.username = input()
            break
        elif option == '2':
            print(EDIT_DETAILS_ASK_PASSWORD)
            profile.password = input()
            break
        elif option == '3':
            print(EDIT_DETAILS_ASK_BIO)
            profile.bio = input()
            break
        elif option == '4':
            print(EDIT_DETAILS_ASK_ADD_POST)
            new_post = Post()
            new_post.entry = input()
            profile.add_post(new_post)
            break
        elif option == '5':
            print(EDIT_DETAILS_ASK_DEL_POST)
            posts = profile.get_posts()[:]
            id = int(input())
            success = profile.del_post(id)
            if success:
                print(f"\tDeleted post ID {id}: {
                    posts[id].get_entry()}")
            else:
                print("EDIT_DETAILS_INDEX_ERROR")
            break
        elif option in ['6', 'q']:
            break
        else:
            print(EDIT_DETAILS_INVALID_OPTION)
    profile.save_profile(path)


"""
Prompts the user to choose between
opening or creating a file. Helps
prevent out-of-order processes within
the custom ui format.
"""


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
ADMIN_ENTER = "Entering admin mode..."


"""
Prints all available options
"""


def print_menu():
    print(COMMAND_OPTIONS_MENU)


"""
Prints a menu all options and allows the user to choose between
all options repeatedly until the user chooses to exit the program.

Options will run their respective functions above and this
function will recursively call itself at the end in order
to repeat the process.
"""


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
    elif option == '6':
        ui_edit(profile, active_path)
    elif option in ['7', 'q']:
        return
    elif option == 'admin':
        print(ADMIN_ENTER)
        ui.run_admin(profile, active_path)
        return

    ui_stage_2(profile, active_path)


JOURNAL_APP_EXIT = "Thank you for using my journal app!"

"""
Starts the user-friendly version of the
journal application.
"""


def run_standard(active_profile: Profile, option: str):
    active_path = ui_stage_1(active_profile, option)
    ui_stage_2(active_profile, active_path)
    active_profile.save_profile(active_path)
    print(JOURNAL_APP_EXIT)
