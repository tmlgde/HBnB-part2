#!/usr/bin/python3
import unittest
import json
from app import create_app
from app.config import DevelopmentConfig
from app.extensions import db
from app.models.user import User


class JWTAuthenticationTestCase(unittest.TestCase):
    """Test JWT login and access to protected endpoint"""

    def setUp(self):
        """Set up test context and database"""
        self.app = create_app(DevelopmentConfig)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Crée un utilisateur test
            user = User(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com"
            )
            user.set_password("testpassword")  # hash automatiquement
            db.session.add(user)
            db.session.commit()

    def test_login_and_protected_access(self):
        """Test login and token access to a protected route"""

        # Étape 1 : Login avec email + mot de passe
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": "john.doe@example.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("access_token", data)

        token = data["access_token"]

        # Étape 2 : Accès au endpoint protégé
        protected_response = self.client.get(
            "/api/v1/protected",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(protected_response.status_code, 200)
        self.assertIn("message", protected_response.get_json())

    def test_invalid_login(self):
        """Test login avec mauvais mot de passe"""
        response = self.client.post(
            "/api/v1/auth/login",
            json={"email": "john.doe@example.com", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
