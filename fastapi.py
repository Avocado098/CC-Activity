import json
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

AUTHORS_BOOKS_CSV = "authors_books.csv"
QUOTES_CSV = "quotes.csv"


class AuthorBook(BaseModel):
    id: int
    author: str
    book: str
    year: int

class Quote(BaseModel):
    id: int
    author: str
    quote: str

def save_author_book(author_book: AuthorBook):
    file_name = AUTHORS_BOOKS_CSV

    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=["id", "author", "book", "year"])
    else:
        df = pd.read_csv(file_name)

    df.loc[len(df)] = [author_book.id, author_book.author, author_book.book, author_book.year]
    df.to_csv(file_name, index=False)

def save_quote(quote: Quote):
    file_name = QUOTES_CSV

    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=["id", "author", "quote"])
    else:
        df = pd.read_csv(file_name)

    df.loc[len(df)] = [quote.id, quote.author, quote.quote]
    df.to_csv(file_name, index=False)

@app.post("/add_author_book")
async def add_author_book(data: AuthorBook):
    save_author_book(data)
    return {
        "message": "Author and book added!",
        "author": data.author,
        "book": data.book,
        "year": data.year
    }

@app.post("/add_quote")
async def add_quote(data: Quote):
    save_quote(data)
    return {
        "message": "Quote added!",
        "author": data.author,
        "quote": data.quote
    }

@app.get("/authors_books")
async def get_all_authors_books():
    if not os.path.exists(AUTHORS_BOOKS_CSV):
        return {"message": "No authors or books found."}

    df = pd.read_csv(AUTHORS_BOOKS_CSV)
    json_df = df.to_json(orient="records")
    return json.loads(json_df)

@app.get("/authors_books/{author}")
async def get_author_books(author: str):
    if not os.path.exists(AUTHORS_BOOKS_CSV):
        return {"message": "No authors or books found."}

    df = pd.read_csv(AUTHORS_BOOKS_CSV)
    df = df[df["author"].str.contains(author, case=False, na=False)]

    if df.empty:
        return {"error": "Author not found"}

    json_df = df.to_json(orient="records")
    return json.loads(json_df)

@app.get("/quotes")
async def get_all_quotes():
    if not os.path.exists(QUOTES_CSV):
        return {"message": "No quotes found."}

    df = pd.read_csv(QUOTES_CSV)
    json_df = df.to_json(orient="records")
    return json.loads(json_df)

@app.get("/quote")
async def get_random_quote():
    if not os.path.exists(QUOTES_CSV):
        return {"message": "No quotes found."}

    df = pd.read_csv(QUOTES_CSV)

    if df.empty:
        return {"message": "No quotes available."}

    df = df.sample()
    json_df = df.to_json(orient="records")
    return json.loads(json_df)