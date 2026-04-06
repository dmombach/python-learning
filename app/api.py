from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello Dan, your API is running!"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}!"}


@app.get("/add")
def add_numbers(a: int, b: int):
    return {"result": a + b}
