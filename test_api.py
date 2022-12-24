import unittest
from app import app
from fastapi.testclient import TestClient
import database

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = database.connect()

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": "Welcome to the Stock API"
        })

    def test_read_all(self):
        response = self.client.get("/stock")
        self.assertEqual(response.status_code, 200)
        length = len(response.json())
        self.assertEqual(length, len(database.select_all(self.db)))
    
    def test_read_by_symbol(self):
        response = self.client.get("/stock/MSFT")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), database.select_by_symbol(self.db, "MSFT"))

    def test_read_by_id(self):
        response = self.client.get("/stock/id/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), database.select_by_id(self.db, 1))

    def test_create(self):
        response = self.client.post("/stock", json={
            "stock_industry": "Technology",
            "stock_market": "NASDAQ",
            "stock_name": "Microsoft",
            "stock_market_cap": "1.6 trillion",
            "stock_symbol": "MSFT"
        })
        self.assertIsNotNone(response.json())

    def test_delete(self):
        response = self.client.delete("/stock/MSFT")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Stock deleted successfully'})

    def tearDown(self):
        self.db.close()

    # Only works if there are no records in the database. Use with caution.
    # def test_delete_all(self):
    #     response = self.client.delete("/stock")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), database.delete_all(self.db))

if __name__ == '__main__':
    unittest.main()
