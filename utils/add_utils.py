import pandas as pd
from fastapi.security import OAuth2PasswordBearer

from exceptions import AppException


class Add:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def validate_parameters(book_name: str, author: str, publication_year: int):
        if not isinstance(book_name, str) or not isinstance(author, str):
            raise AppException("Book Name and Author must be strings!")
        if not isinstance(publication_year, int) or publication_year < 1000 or publication_year > 9999:
            raise AppException("Publication Year must be a valid 4-digit number!")

    @staticmethod
    def add_book_to_csv(book_name: str, author: str, publication_year: int):
        df = pd.read_csv("/home/nupur_khare/PycharmProjects/Library/data/regular_users.csv", encoding="utf8", sep=",")
        new_row = {"Book Name": book_name, "Author": author, "Publication Year": publication_year}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("/home/nupur_khare/PycharmProjects/Library/data/regular_users.csv", index=False)
