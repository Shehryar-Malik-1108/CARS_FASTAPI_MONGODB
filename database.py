import pymongo


class MyDatabase:
    def __init__(self):
        self.db = self.get_db()

    def get_db(self, db_name="car_db"):
        client = pymongo.MongoClient(f"mongodb://127.0.0.1:27017/{db_name}")
        if db_name not in client.list_database_names():
            print(f"Database '{db_name}' not found, creating...")
            db = client[db_name]
            db.create_collection("cars")

        db = client.get_database(db_name)

        print(f"Returning DB: {db_name}")
        return db

    def select_car(self, id: int):
        col = self.db.get_collection("cars")
        car1 = col.find_one({"id": id})
        return car1

    def get_all_cars(self):
        col = self.db.get_collection("cars")
        cars = []
        for car in col.find():
            cars.append(car)
        return {"cars": cars}

    def insert_car(self, id: int, name: str, cc: int, color: str, price: int, cars=None):
        col = self.db.get_collection("cars")

        if cars is None:

            new_car = col.insert_one({"id": id, "name": name, "cc": cc, "color": color, "price": price})
            if new_car.acknowledged:
                return f"Car {name} created"
        else:

            new_cars = col.insert_many([car.dict() for car in cars])
            if new_cars.acknowledged:
                return {"message": f"{len(new_cars.inserted_ids)} car created"}

        return f"Error occurred while creating new car {name}."

    def insert_many_cars(self, cars: list[dict]):
        col = self.db.get_collection("cars")
        new_cars = col.insert_many([car for car in cars])
        if new_cars.acknowledged:
            return f"{len(new_cars.inserted_ids)} cars created"
        return {"Error occurred while creating new cars."}

    def update_car(self, id: int, price: int):
        col = self.db.get_collection("cars")
        car_dict = {k: v for k, v in {"price": price}.items() if v is not None}
        result = col.update_one({"id": id}, {"$set": car_dict})
        if result.modified_count == 1:
            return f"{id} Car updated."
        return None

    def update_many_cars(self, cars: list[dict]):
        col = self.db.get_collection("cars")
        result = col.update_many(
            {"id": {"$in": [b['id'] for b in cars]}},
            {"$set": {k: v for b in cars for k, v in b.items() if k != 'id' and v is not None}}
        )
        if result.modified_count > 0:
            return {"message": f"{result.modified_count} cars updated."}
        return {"message": "No cars updated."}

    def delete_car(self, id: int):
        col = self.db.get_collection("cars")
        result = col.delete_one({"id": id})
        if result.deleted_count == 1:
            return f"{id}Cars deleted"
        return f"error occurred while deleting cars {id}."

    def delete_many_cars(self, cars: list[int]):
        col = self.db.get_collection("cars")
        result = col.delete_many({"id": {"$in": cars}})
        if result.deleted_count > 0:
            return f"{result.deleted_count} cars deleted."
        return {"message": "No Cars deleted."}


if __name__ == "__main__":
    pass
