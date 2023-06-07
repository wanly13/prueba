from fastapi import FastAPI
from src.search import find_tweetids as search


app = FastAPI()

#http://localhost:8000/
@app.get("/")
def read_root():
    return search(str("Prueba"), int(5))


#http://localhost:8000/items/42?q=test
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return search(str("Prueba"), int(5))