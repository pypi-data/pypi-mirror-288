#coding: utf-8
from typing import Optional
from typing import Union

def codeBlocksParser(data: Union[str, bytes], language: Optional[Union[str, bytes, list]] = None) -> list:
    """
    Parses code blocks from the given data and filters them based on the specified language(s).

    Args:
        data (str|bytes): The input data containing code blocks.
        language (str|bytes|list|None, optional): The language(s) to filter the code blocks. Defaults to None.

    Returns:
        list: A list of dictionaries representing the parsed code blocks, each containing the language and code.

    Example:
        data = '''
        Some text before the code block.

        ```python
        def hello_world():
            print("Hello, World!")
        ```

        Some text after the code block.
        '''

        parsed_blocks = codeBlocksParser(data, language='python')
        print(parsed_blocks)
        # Output: [{'language': 'python', 'code': 'def hello_world():\n    print("Hello, World!")'}]
    """
    import re

    # function to convert bytes to string
    def bytes_to_string(data: bytes) -> str:
        """
        Converts a bytes object to a string.

        Args:
            data (bytes): The bytes object to be converted.

        Returns:
            str: The string representation of the bytes object.
        """
        return data.decode()

    # function with regex to match code blocks into a string
    def match_code_blocks(data: Union[str, bytes]) -> list:
        """
        Extracts code blocks from the given data.

        Args:
            data (str|bytes): The input data to search for code blocks.

        Returns:
            list: A list of code blocks found in the data.
        """
        return re.findall(r"```(.+?)```", data, re.DOTALL)

    # function to match single code blocks
    def match_single_code_blocks(data: Union[str, bytes]) -> list:
        """
        Match and return a list of individual code blocks delimited by backticks (`) in the given data.

        Args:
            data (str|bytes): The input data to search for code blocks.

        Returns:
            list: A list of individual code blocks found in the data.

        Example:
            >>> data = "This is a `code block` example."
            >>> match_single_code_blocks(data)
            ['code block']
        """
        return re.findall(r"`([^`\n]+)`", data)

    def split_code_block(code_block: str) -> dict:
        """
        Splits a code block into its language and code content.

        Args:
            code_block (str): The code block to be split.

        Returns:
            dict: A dictionary containing the language and code content of the code block.
        """
        block = code_block.split('\n')
        # remove the first line if it is empty
        # and define the language if it is not defined
        if block[0] == '':
            language = None
            block = block[1:]
        elif block[0] != '':
            language = block[0]
            block = block[1:]
        # remove the last line if it is empty
        if block[-1] == '':
            block = block[:-1]
        return {
            'language': language,
            'code': '\n'.join(block)
        }

    def parse_blocks(data: Union[str, bytes]) -> dict:
        """
        Parse the given data and extract single code blocks and code blocks.

        Args:
            data (str|bytes): The data to be parsed. It can be either a string or bytes.

        Returns:
            dict: A dictionary containing the extracted single code blocks and code blocks.
                The 'single_code_blocks' key maps to a list of single code blocks.
                The 'code_blocks' key maps to a list of split code blocks.
        """
        if type(data) == bytes:
            data = bytes_to_string(data)

        single_code_blocks = match_single_code_blocks(data)
        code_blocks = match_code_blocks(data)
        splited_code_blocks = [split_code_block(block) for block in code_blocks]
        return {
            'single_code_blocks': single_code_blocks,
            'code_blocks': splited_code_blocks
        }

    def keep_only_blocks_by_language(parsed_blocks: dict, language: Optional[Union[str, bytes, list]] = None) -> dict:
        """
        Filters the parsed code blocks based on the specified language(s).

        Args:
            parsed_blocks (dict): The dictionary containing the parsed code blocks.
            language (str|bytes|list|None): The language(s) to filter the code blocks by. 
                It can be a single language string, a list of language strings, bytes, or None.

        Returns:
            dict: A dictionary containing the filtered code blocks.

        """
        if language == None:
            return parsed_blocks
        elif type(language) == str:
            language = [language]
        elif type(language) == bytes:
            language = [language.decode()]

        keeped_blocks = []
        for parsed_block in parsed_blocks['code_blocks']:
            if parsed_block['language'] in language:
                keeped_blocks.append(parsed_block)
        return {
            'single_code_blocks': parsed_blocks['single_code_blocks'],
            'code_blocks': keeped_blocks
        }

    # ############# MAIN FUNCTION #############
    parsed_blocks = parse_blocks(data)
    return keep_only_blocks_by_language(parsed_blocks, language)
