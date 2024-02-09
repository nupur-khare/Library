import unittest
from unittest.mock import patch

import pandas as pd
import pytest

from exceptions import AppException
from utils.add_utils import Add


class TestAdd(unittest.TestCase):

    def test_add_book_to_csv_success(self):
        Add.add_book_to_csv("Book1", "Author1", 2000)

    def test_validate_parameters_success(self):
        Add.validate_parameters("Book1", "Author1", 2000)

    def test_validate_parameters_invalid_type(self):
        with pytest.raises(AppException, match="Book Name and Author must be strings!"):
            Add.validate_parameters(123, 456, 2000)

    def test_validate_parameters_invalid_year(self):
        with pytest.raises(AppException, match="Publication Year must be a valid 4-digit number!"):
            Add.validate_parameters("Book1", "Author1", 999)
