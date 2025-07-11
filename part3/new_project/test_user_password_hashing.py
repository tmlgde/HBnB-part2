#!/usr/bin/python3
"""
Unittest for password hashing and User endpoints
"""
import unittest
import json
import uuid
from app import create_app, db
from app.models.user import User


class TestUserPasswordHashing(unittest.TestCase):
    """Test case for user password hashing and endpoint protection"""

    def setUp(self):
        """Set up test client and database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clear DB after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_password_is_hashed_in_database(self):
        """Test that password is hashed and not stored in plaintext"""
        payload = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "mysecret"
        }

        response = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(response.status_code, 201)

        with self.app.app_context():
            user = User.query.filter_by(email="test@example.com").first()
            self.assertIsNotNone(user)
            self.assertNotEqual(user.password, "mysecret")
            self.assertTrue(user.verify_password("mysecret"))
            self.assertFalse(user.verify_password("wrongpassword"))

    def test_password_not_returned_on_post(self):
        """Ensure password is not in response after registration"""
        payload = {
            "email": "secure@example.com",
            "first_name": "Sec",
            "last_name": "Ure",
            "password": "mypassword"
        }

        response = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertNotIn("password", data)
        self.assertIn("id", data)
        self.assertIn("message", data)

    def test_password_not_returned_on_get(self):
        """Ensure password is not exposed in GET user/<id>"""
        with self.app.app_context():
            user = User(
                id=str(uuid.uuid4()),
                email="get@example.com",
                first_name="Get",
                last_name="User"
            )
            user.hash_password("getpass")
            db.session.add(user)
            db.session.commit()
            user_id = user.id  # stocker l'ID ici car `user` ne sera plus valide après

        response = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertNotIn("password", data)
        self.assertEqual(data["email"], "get@example.com")


if __name__ == '__main__':
    unittest.main()
