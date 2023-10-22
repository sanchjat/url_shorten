import os
import hashlib
from pymongo import MongoClient
from short_url.utils import base62_encode
from pymongo.errors import DuplicateKeyError

db = None
client = None


class BaseModel:
    def __init__(self, collection="User"):
        self.collection = self.reconnect(collection)

    def reconnect(self, collection):
        global db, client
        if db is None or client is None:
            if os.environ.get("APP_ENV") in ["PROD"]:
                db_url = os.environ["DB_URL"]
                db_username = os.environ["DB_USERNAME"]
                db_password = os.environ["DB_PASSWORD"]
                client = MongoClient("Prod DB URL")

            else:
                host = os.environ.get("DB_HOST", "mongodb")
                db_username = os.environ["DB_USERNAME"]
                db_password = os.environ["DB_PASSWORD"]
                port = 27017
                client = MongoClient(
                    f"mongodb://{host}:{port}/",
                    username=db_username,
                    password=db_password,
                )
        db = client["short_url"]
        self.collection = db[collection]
        return self.collection

    def get_mongo_client(self):
        if client:
            return client
        else:
            self.reconnect(self.collection)
            return client


# TODO temp store user data here instead of DB
user_data = {
    "admin@admin.com": {
        "_id": 123,
        "password": hashlib.md5(b"admin"),
        "active": True,
        "is_admin": False,
    }
}


class User(BaseModel):
    def __init__(self, collection="User"):
        super().__init__(collection)

    def is_admin():
        pass

    def create_user(self, user_obj):
        pass

    def get_by_id(self, user_id):
        for email, user in user_data.items():
            if user["_id"] == user_id:
                return user

    def login(self, email, password):
        user = user_data.get(email)
        if user["password"].hexdigest() == hashlib.md5(password.encode()).hexdigest():
            return user

    def delete_user(self):
        pass


class Counter(BaseModel):
    def __init__(self, collection="Counter"):
        super().__init__(collection)

    def one(self, filter):
        mongo_client = self.get_mongo_client()
        with mongo_client.start_session() as session:
            obj = self.collection.find_one(filter, session=session)
            return obj

    def save(self, obj):
        self.collection.find_one_and_update({"type": "counter"}, {"$set": obj})


class Url(BaseModel):
    # url.collection.create_index('short_key', unique = True)
    def __init__(self, collection="Url"):
        super().__init__(collection)

    def find_by_short_key(self, short_key):
        mongo_client = self.get_mongo_client()
        with mongo_client.start_session() as session:
            return self.collection.find_one({"short_key": short_key}, session=session)

    def create_short_url(self, url_obj):
        mongo_client = self.get_mongo_client()
        with mongo_client.start_session() as session:
            counter_obj = Counter().one({"type": "counter"}) or {
                "type": "counter",
                "value": 1000,
            }
            # To avoid a condition when 10 URLs created at same time
            for i in range(10):
                try:
                    counter_obj["value"] += 1
                    url_obj["short_key"] = base62_encode(counter_obj["value"])
                    print(url_obj)
                    obj = self.collection.insert_one(url_obj, session=session)
                    Counter().save(counter_obj)
                    return url_obj["short_key"]
                except DuplicateKeyError as e:
                    pass
            raise Exception("Unable to create short url due to duplicate records")

    def is_valid(self):
        """This method will check URL is active or not"""
        pass
