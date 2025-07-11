#!/usr/bin/python3
import unittest
import sqlite3


class TestShemaSQL(unittest.TestCase):
    """Tests pour vérifier la structure et les données initiales"""

    def setUp(self):
        self.conn = sqlite3.connect("dev.db")
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_tables_exist(self):
        expected_tables = {'users', 'places', 'reviews', 'amenities', 'place_amenity'}
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in self.cursor.fetchall()}
        for table in expected_tables:
            self.assertIn(table, tables, f"Table '{table}' manquante")

    def test_admin_user_exists(self):
        self.cursor.execute("""
            SELECT id, email, first_name, last_name, is_admin, password
            FROM users
            WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
        """)
        user = self.cursor.fetchone()
        self.assertIsNotNone(user, "Utilisateur admin manquant")
        self.assertEqual(user[1], "admin@hbnb.io")
        self.assertEqual(user[2], "Admin")
        self.assertEqual(user[3], "HBnB")
        self.assertTrue(user[4], "is_admin devrait être TRUE")
        self.assertTrue(user[5].startswith("$2b$") or user[5].startswith("$2a$"), "Mot de passe non hashé en bcrypt")

    def test_initial_amenities(self):
        self.cursor.execute("SELECT name FROM amenities;")
        amenities = {row[0] for row in self.cursor.fetchall()}
        expected = {"WiFi", "Swimming Pool", "Air Conditioning"}
        for item in expected:
            self.assertIn(item, amenities, f"Amenity '{item}' manquant")


if __name__ == '__main__':
    unittest.main()
