import unittest

import pytest

from exceptions import AppException
from utils.delete_utils import Delete


class TestDelete(unittest.TestCase):

    def test_delete_book_from_csv_success(self):
        Delete.delete_book_from_csv("Don Quixote")

    def test_validate_parameters_success(self):
        Delete.validate_parameters("Book1")

    def test_validate_parameters_invalid_type(self):
        with pytest.raises(AppException, match="Book Name must be a string!"):
            Delete.validate_parameters(123)
