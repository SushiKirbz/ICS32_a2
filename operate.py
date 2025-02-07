# Luke Phimphisane
# lphimphi@uci.edu
# 72686112

from pathlib import Path
from Profile import Profile, Post
import os


def create_file(path: str):
    """
    Creates a file at the given path.
    Parameters:
    path - a Path object of the desired location for file creation.
    """
    file_path = Path(path)
    file_path.touch(exist_ok=False)
    print(file_path.resolve())


def open_file(profile: Profile, path: str):
    profile.load_profile(path)


def delete_file(path):
    """
    Deletes a file at the given path.
    Parameters:
    path - a Path object of the desired location for file creation.
    """
    file_path = path
    try:
        file_path.unlink()
        print(f'{file_path} DELETED')
    except FileNotFoundError:
        print("ERROR")


def read_file(path):
    """
    Reads a file at the given path line by line. Will print "EMPTY" if file size is zero.
    All contained whitespace characters will count as a non-empty file.
    Parameters:
    path - a Path object of the desired location for file creation.
    """
    file_path = path
    try:
        with file_path.open() as file:
            if os.path.getsize(file_path) == 0:
                print("EMPTY")
            else:
                for line in file:
                    print(line.rstrip('\n'))
    except FileNotFoundError:
        print("ERROR")


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
            print(f'  ID {i}: {post._entry}')
    elif option == '-post':
        try:
            print(profile.get_posts()[int(argument)].get_entry())
        except ValueError:
            print("ERROR")
        except IndexError:
            print("ERROR")
    elif option == '-all':
        print(f"Username: {profile.username}")
        print(f"Password: {profile.password}")
        print(f"Bio: {profile.bio}")
        print("All posts:")
        for i, post in enumerate(profile.get_posts()):
            print(f'  ID {i}: {post.get_entry()}')
    else:
        print("ERROR")


def parse_edit_options(profile: Profile, input: list):

    option = input[0]
    argument = input[1]

    if option == '-usr':
        profile.username = argument
    elif option == '-pwd':
        profile.password = argument
    elif option == '-bio':
        profile.bio = argument
    elif option == '-addpost':
        new_post = Post()
        new_post.entry = argument
        profile.add_post(new_post)
    elif option == '-delpost':
        posts = profile.get_posts()[:]
        success = profile.del_post(int(argument))
        if success:
            print(f"\tDeleted post ID {int(argument)}: {
                  posts[int(argument)].get_entry()}")
        else:
            print("ERROR")
    else:
        print("ERROR")
