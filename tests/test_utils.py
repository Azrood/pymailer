import unittest
import os

from src.utils import replce


class TestMappingCSV(unittest.TestCase):
    def setUp(self):
        pass


class testReplace(unittest.TestCase):
    def test_replce_from_text_file(self):
        context = {'name': 'Python', 'company': 'PSF'}
        fp = os.path.join(os.path.expanduser('~'),os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"example/mailtext.sample.txt")
        expected_text = "Hello Python\nI am looking for a job/internship/something, I hope I will work in PSF.\nThanks"
        self.assertEqual(replce(fp, context), expected_text)
