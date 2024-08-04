import unittest
from BorgTestGenerator.utils.files import read_text_file

class TestFiles(unittest.TestCase):
    def test_read_text_file(self):
        from os import urandom
        with open("/tmp/case_1.txt", "w") as f:
            f.write("This is the content of the file.")
            f.close()
        # Test case 1: Existing file
        file_path = "/tmp/case_1.txt"
        expected_output = "This is the content of the file."
        self.assertEqual(read_text_file(file_path), expected_output)

        # Test case 2: Non-existing file ( exception : FileNotFoundError )
        file_path = "/tmp/case_2.txt"
        with self.assertRaises(FileNotFoundError):
            read_text_file(file_path)
        

if __name__ == "__main__":
    unittest.main()