import pymongo
import dotenv

# Ensure the script can find the .env file anywhere
dotenv.load_dotenv(dotenv.find_dotenv())


class MongoDBClient:
    """MongoDB Client to manage connections and retrieve collections."""

    def __init__(self, mongodb_uri: str, db_name: str, collection_name: str):
        """
        Initialize MongoDB connection.

        Args:
            mongodb_uri (str): The MongoDB connection URI.
            db_name (str): The database name.
            collection_name (str): The collection name.
        """
        self.mongo_uri = mongodb_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self.connect_mongodb()

    def connect_mongodb(self):
        """Establish a connection to MongoDB."""
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            print(f"Connected to MongoDB. Collection '{self.collection_name}' ready.")
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB connection error: {e}")

    def get_collection(self):
        """
        Retrieve the MongoDB collection.

        Returns:
            pymongo.collection.Collection: The collection object.
        """
        return self.collection


if __name__ == "__main__":
    import os

    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    db_name = "product"
    collection_name = "sendo"

    mongo_client = MongoDBClient(mongodb_uri, db_name, collection_name)
