#coding: utf-8

# import pkg_resources
from os import path

from typing import Union

def read_text_file(file_path: str) -> Union[str, None]:
    """
    Read the contents of a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str|None: The contents of the text file as a string, or None if the file does not exist.
    """
    if not path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est manquant")
    
    with open(file_path, 'r') as in_file:
        return in_file.read()