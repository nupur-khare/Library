import unittest

from utils.home_utils import Home


class TestReadBooksFromCSV(unittest.TestCase):

    def test_read_books_from_csv(self):
        file_path = "/home/nupur_khare/PycharmProjects/Library/tests/testing_data/test.csv"
        expected_books = [
            "Don Quixote",
            "A Tale of Two Cities",
            "The Lord of the Rings",
            "The Little Prince",
            "Harry Potter and the Sorcerer’s Stone",
            "And Then There Were None",
            "The Dream of the Red Chamber",
            "The Hobbit",
            "She: A History of Adventure",
            "The Lion the Witch and the Wardrobe"
        ]
        actual_books = Home.read_books_from_csv([file_path])
        self.assertEqual(actual_books, expected_books)
