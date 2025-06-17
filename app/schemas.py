from datetime import datetime

class AuthorDetailSchema():
    id: int
    name: str
    bio:str
    books: list["BookDetailSchema"]


class BookDetailSchema():
    id: int
    title: str
    summary: str
    publication_date: datetime
    author_id: int
