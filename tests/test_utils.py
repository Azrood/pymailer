import unittest
import os

from src.utils import replce, mapping_csv, select_smtp_provider

BASE_DIR_EXAMPLE = os.path.join(os.path.expanduser('~'),
                                os.path.dirname(
                                    os.path.dirname(
                                        os.path.abspath(__file__))))


class TestMappingCSV(unittest.TestCase):
    def test_mapping_csv(self):
        row = {'name': 'John',
               'company': 'mycompany',
               'email': 'email@mail.com'}

        expected_mapping = [
                    {
                     'name': 'John',
                     'company': 'mycompany',
                     'email': 'email@mail.com'
                    },
                    {
                     'name': 'Python',
                     'company': 'good company',
                     'email': 'mail@mail.mail'},
                    {
                        'name': '',
                        'company': '',
                        'email': 'another@mail.com'},
                    {
                        'name': 'Bob',
                        'company': '',
                        'email': 'thismail@broken.com',
                    }

                    ]
        fp = os.path.join(BASE_DIR_EXAMPLE,
                          "example/database_example.csv")

        context = mapping_csv(fp)
        self.assertIn(row, context)
        self.assertEqual(context, expected_mapping)

    def test_mapping_csv_fields(self):
        fp = os.path.join(BASE_DIR_EXAMPLE,
                          "example/database_example.csv")

        row_context = mapping_csv(fp)[0]
        with open(fp) as f:
            fieldnames = f.readline().strip().split(',')

        self.assertTrue(all(field.lower() in fieldnames
                            for field in row_context))

        self.assertIn("email", fieldnames)
        self.assertIn("email", row_context)


class testReplace(unittest.TestCase):
    def test_replce_from_text_file(self):
        context = {'name': 'Python', 'company': 'PSF'}
        fp = os.path.join(BASE_DIR_EXAMPLE,
                          "example/mailtext.sample.txt")

        expected_text = ("Hello Python\nI am looking for a job/internship/"
                         "something, I hope I will work in PSF.\nThanks")
        self.assertEqual(replce(fp, context), expected_text)


class testSelectSMTPAddress(unittest.TestCase):
    def test_select_smtp_provider(self):
        mail = "user@gmail.com"
        smtp, port = select_smtp_provider(mail)
        expected_values = ("smtp.gmail.com", 465)
        self.assertEqual((smtp, port), expected_values)
