
import unittest
from backend.chatbot.getCollection import GetCollection
import dotenv

class TestGetCollection(unittest.TestCase):
    def setUp(self):
        # Load environment variables from .env file
        env = dotenv.dotenv_values('.env')
        self.mongo_uri = env.get('MONGO_URI')
        self.db_name = env.get('DB_NAME')
        self.collection_name = env.get('COLLECTION_NAME')

    def test_init_with_valid_parameters(self):
        get_collection = GetCollection(self.mongo_uri, self.db_name, self.collection_name)
        
        self.assertEqual(get_collection.mongo_uri, self.mongo_uri)
        self.assertEqual(get_collection.dbName, self.db_name)
        self.assertEqual(get_collection.collection_name, self.collection_name)
        self.assertIsNone(get_collection.db)
        self.assertIsNone(get_collection.collection)
        self.assertIsNotNone(get_collection.client)

if __name__ == '__main__':
    unittest.main()