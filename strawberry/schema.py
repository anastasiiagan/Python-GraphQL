import typing
import strawberry


@strawberry.type
class Book:
    title: str
    author: str


def get_books():
    return [Book(title="ABC", author="grammer"), Book(title="title", author="author")]


@strawberry.type
class Query:
    book: typing.List[Book] = strawberry.field(resolver=get_books)


schema = strawberry.Schema(query=Query)
