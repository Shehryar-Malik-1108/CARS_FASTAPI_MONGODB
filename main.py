import pydantic
from bson import ObjectId
from fastapi import FastAPI
from database import MyDatabase

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI(title="Shehryar ki Gariyan")
db = MyDatabase()


@app.get("/")
def home():
    return {"message": "Welcome to Shehryar ki Dukaan!!"}


@app.get("/Select_Car")
def select_car(id: int):
    return db.select_car(id)


@app.get("/All_Cars")
def get_all_cars():
    return db.get_all_cars()


@app.post("/Insert_Car")
def insert_car(id: int, name: str, cc: int, color: str, price: int):
    return db.insert_car(id, name, cc, color, price)


@app.post("/Insert_Many_Cars")
def insert_many_cars(cars: list):
    return db.insert_many_cars(cars)


@app.put("/Update_Car")
def update_car(id: int, price: int):
    return db.update_car(id, price)


@app.put("/Update_Many_Cars")
def update_many_cars(cars: list[dict]):
    return db.update_many_cars(cars)


@app.delete("/Delete_Car")
def delete_car(id: int):
    return db.delete_car(id)


@app.delete("/Delete_Many_Cars")
def delete_many_cars(cars: list[int]):
    return db.delete_many_cars(cars)
