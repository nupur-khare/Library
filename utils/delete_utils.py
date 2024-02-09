import pandas as pd

from exceptions import AppException


class Delete:

    @staticmethod
    def validate_parameters(book_name: str):
        if not isinstance(book_name, str):
            raise AppException("Book Name must be a string!")

    @staticmethod
    def delete_book_from_csv(book_name: str):
        df = pd.read_csv("/home/nupur_khare/PycharmProjects/Library/data/regular_users.csv", encoding="utf8", sep=",")
        df = df[df["Book Name"].str.lower() != book_name.lower()]
        df.to_csv("/home/nupur_khare/PycharmProjects/Library/data/regular_users.csv", index=False)
        