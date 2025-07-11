
import unittest
import sqlite3

class TestRelationships(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect("dev.db")
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_user_place_relationship(self):
        self.cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='places'
        """)
        create_stmt = self.cursor.fetchone()
        self.assertIsNotNone(create_stmt)
        self.assertIn("owner_id", create_stmt[0])
        self.assertIn("REFERENCES users(id)", create_stmt[0])

    def test_place_review_relationship(self):
        self.cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='reviews'
        """)
        create_stmt = self.cursor.fetchone()
        self.assertIsNotNone(create_stmt)
        self.assertIn("place_id", create_stmt[0])
        self.assertIn("REFERENCES places(id)", create_stmt[0])

    def test_user_review_relationship(self):
        self.cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='reviews'
        """)
        create_stmt = self.cursor.fetchone()
        self.assertIsNotNone(create_stmt)
        self.assertIn("user_id", create_stmt[0])
        self.assertIn("REFERENCES users(id)", create_stmt[0])

    def test_place_amenity_relationship(self):
        self.cursor.execute("""
            SELECT sql FROM sqlite_master 
            WHERE type='table' AND name='place_amenity'
        """)
        create_stmt = self.cursor.fetchone()
        self.assertIsNotNone(create_stmt)
        self.assertIn("FOREIGN KEY (place_id) REFERENCES places(id)", create_stmt[0])
        self.assertIn("FOREIGN KEY (amenity_id) REFERENCES amenities(id)", create_stmt[0])

if __name__ == '__main__':
    unittest.main()
