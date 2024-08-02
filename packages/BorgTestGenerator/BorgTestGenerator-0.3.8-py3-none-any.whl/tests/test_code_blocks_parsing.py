# import unittest
# from BorgTestGenerator.parsers.code_blocks_parsing import codeBlocksParser

# class TestCodeBlocksParser(unittest.TestCase):
#     def test_code_blocks_parser(self):
#         # Test case 1: Single code block with specified language
#         data = '''
#         Some text before the code block.

#         ```python
#         def hello_world():
#             print("Hello, World!")
#         ```

#         Some text after the code block.
#         '''
#         expected_output = [{'language': 'python', 'code': 'def hello_world():\n    print("Hello, World!")'}]
#         self.assertEqual(codeBlocksParser(data, language='python'), expected_output)

#         # Test case 2: Multiple code blocks with specified language
#         data = '''
#         Some text before the code blocks.

#         ```python
#         def hello_world():
#             print("Hello, World!")
#         ```

#         Some text in between.

#         ```python
#         def goodbye_world():
#             print("Goodbye, World!")
#         ```

#         Some text after the code blocks.
#         '''
#         expected_output = [
#             {'language': 'python', 'code': 'def hello_world():\n    print("Hello, World!")'},
#             {'language': 'python', 'code': 'def goodbye_world():\n    print("Goodbye, World!")'}
#         ]
#         self.assertEqual(codeBlocksParser(data, language='python'), expected_output)

#         # Test case 3: Single code block without specified language
#         data = '''
#         Some text before the code block.

#         ```
#         def hello_world():
#             print("Hello, World!")
#         ```

#         Some text after the code block.
#         '''
#         expected_output = [{'language': None, 'code': 'def hello_world():\n    print("Hello, World!")'}]
#         self.assertEqual(codeBlocksParser(data), expected_output)

#         # Test case 4: Multiple code blocks without specified language
#         data = '''
#         Some text before the code blocks.

#         ```
#         def hello_world():
#             print("Hello, World!")
#         ```

#         Some text in between.

#         ```
#         def goodbye_world():
#             print("Goodbye, World!")
#         ```

#         Some text after the code blocks.
#         '''
#         expected_output = [
#             {'language': None, 'code': 'def hello_world():\n    print("Hello, World!")'},
#             {'language': None, 'code': 'def goodbye_world():\n    print("Goodbye, World!")'}
#         ]
#         self.assertEqual(codeBlocksParser(data), expected_output)

#         # Test case 5: No code blocks
#         data = '''
#         Some text without any code blocks.
#         '''
#         expected_output = {'single_code_blocks': [], 'code_blocks': []}
#         self.assertEqual(codeBlocksParser(data), expected_output)

# if __name__ == "__main__":
#     unittest.main()