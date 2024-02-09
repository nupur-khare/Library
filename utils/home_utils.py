from typing import List

import pandas as pd


class Home:

    @staticmethod
    def read_books_from_csv(file_paths: List[str]) -> List[str]:
        books = []
        for file_path in file_paths:
            df = pd.read_csv(file_path, encoding="utf8", sep=",")
            books.extend(df['Book Name'].tolist())
        return books
