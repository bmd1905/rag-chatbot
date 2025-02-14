import unittest
from unittest.mock import patch, MagicMock
from get_collection import MongoDBClient
import pymongo
import dotenv
import os

################################################################
dotenv.load_dotenv(dotenv.find_dotenv())
################################################################


class TestMongoDBClient(unittest.TestCase):
    @patch("pymongo.MongoClient")
    def test_successful_connection(self, mock_mongo_client):
        """
        Test the successful connection to MongoDB using MongoDBClient.
        """
        mock_client_instance = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()

        # Mock the database and collection access
        mock_mongo_client.return_value = mock_client_instance
        mock_client_instance.__getitem__.side_effect = lambda db: mock_db if db == "product" else MagicMock()
        mock_db.__getitem__.side_effect = lambda col: mock_collection if col == "sendo" else MagicMock()

        mongodb_uri = os.getenv("MONGODB_URI")
        db_name = "product"
        collection_name = "sendo"

        client = MongoDBClient(mongodb_uri, db_name, collection_name)

        mock_mongo_client.assert_called_once_with(mongodb_uri)
        self.assertEqual(client.db_name, db_name)
        self.assertEqual(client.collection_name, collection_name)
        self.assertIsNotNone(client.client)
        self.assertIsNotNone(client.db)
        self.assertIsNotNone(client.collection)

    @patch("pymongo.MongoClient")
    def test_create_collection_with_specified_name(self, mock_mongo_client):
        """
        Test that a specified collection is correctly created and accessed.
        """
        mock_client_instance = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()

        # Mock the database and collection access
        mock_mongo_client.return_value = mock_client_instance
        mock_client_instance.__getitem__.side_effect = lambda db: mock_db if db == "test_db" else MagicMock()
        mock_db.__getitem__.side_effect = lambda col: mock_collection if col == "test_collection" else MagicMock()

        mongodb_uri = "mongodb://localhost:27017/"
        db_name = "test_db"
        collection_name = "test_collection"

        client = MongoDBClient(mongodb_uri, db_name, collection_name)

        mock_mongo_client.assert_called_once_with(mongodb_uri)
        mock_db.__getitem__.assert_called_once_with(collection_name)
        self.assertEqual(client.collection, mock_collection)

    @patch("pymongo.MongoClient")
    def test_connect_to_nonexistent_database(self, mock_mongo_client):
        """
        Test handling of a nonexistent database connection.
        """
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance

        # Simulate an error when trying to access a database
        mock_client_instance.__getitem__.side_effect = pymongo.errors.OperationFailure("Database not found")

        mongodb_uri = "mongodb://localhost:27017/"
        db_name = "nonexistent_db"
        collection_name = "test_collection"

        with patch("builtins.print") as mock_print:
            client = MongoDBClient(mongodb_uri, db_name, collection_name)

            self.assertIsNone(client.collection)
            mock_print.assert_called_with("MongoDB connection error: Database not found")


if __name__ == "__main__":
    unittest.main()
