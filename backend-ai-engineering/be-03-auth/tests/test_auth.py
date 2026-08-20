import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Set dummy env vars
os.environ["SUPABASE_URL"] = os.environ.get("SUPABASE_URL", "https://xyzcompany.supabase.co")
# A well-formed dummy JWT structure (header.payload.signature)
dummy_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5emNvbXBhbnkiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYwMDAwMDAwMCwiZXhwIjoxOTAwMDAwMDAwfQ.signature"
os.environ["SUPABASE_KEY"] = os.environ.get("SUPABASE_KEY", dummy_jwt)

from fastapi.testclient import TestClient
from app.main import app
import app.deps as deps
import app.routes.auth as auth_route


class TestAuthAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_public_info(self):
        resp = self.client.get("/public/info")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"message": "Welcome stranger! This info is public."})

    def test_signup_missing_email(self):
        resp = self.client.post("/auth/signup", json={"email": "", "password": "password123"})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["detail"], "Email and password are required")

    def test_signup_missing_password(self):
        resp = self.client.post("/auth/signup", json={"email": "test@example.com", "password": ""})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["detail"], "Email and password are required")

    def test_login_missing_fields(self):
        resp = self.client.post("/auth/login", json={"email": "", "password": ""})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["detail"], "Email and password are required")

    def test_protected_profile_no_token(self):
        resp = self.client.get("/protected/profile")
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json()["detail"], "Access token required")

    def test_protected_dashboard_no_token(self):
        resp = self.client.get("/protected/dashboard")
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json()["detail"], "Access token required")

    def test_protected_profile_invalid_token(self):
        with mock.patch.object(deps.supabase.auth, "get_user", side_effect=Exception("Invalid token")):
            resp = self.client.get("/protected/profile", headers={"Authorization": "Bearer invalid_token"})
            self.assertEqual(resp.status_code, 401)
            self.assertEqual(resp.json()["detail"], "Invalid or expired token")

    def test_protected_profile_valid_token(self):
        mock_user = mock.Mock()
        mock_user.id = "user-123"
        mock_user.email = "test@example.com"
        mock_user.created_at = "2026-08-20T00:00:00Z"
        
        mock_response = mock.Mock()
        mock_response.user = mock_user

        with mock.patch.object(deps.supabase.auth, "get_user", return_value=mock_response):
            resp = self.client.get("/protected/profile", headers={"Authorization": "Bearer valid_jwt_token"})
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertEqual(data["id"], "user-123")
            self.assertEqual(data["email"], "test@example.com")
            self.assertEqual(data["created_at"], "2026-08-20T00:00:00Z")

    def test_protected_dashboard_valid_token(self):
        mock_user = mock.Mock()
        mock_user.id = "user-123"
        mock_user.email = "test@example.com"
        
        mock_response = mock.Mock()
        mock_response.user = mock_user

        with mock.patch.object(deps.supabase.auth, "get_user", return_value=mock_response):
            resp = self.client.get("/protected/dashboard", headers={"Authorization": "Bearer valid_jwt_token"})
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertIn("Welcome test@example.com", data["message"])

    def test_signup_successful(self):
        mock_res = mock.Mock()
        mock_res.user = {"id": "user-456", "email": "new@example.com"}

        with mock.patch.object(auth_route.supabase.auth, "sign_up", return_value=mock_res):
            resp = self.client.post("/auth/signup", json={"email": "new@example.com", "password": "password123"})
            self.assertEqual(resp.status_code, 201)
            self.assertIn("user", resp.json())

    def test_login_successful(self):
        mock_session = mock.Mock()
        mock_session.access_token = "mock_access_token_xyz"
        mock_session.refresh_token = "mock_refresh_token_xyz"
        
        mock_res = mock.Mock()
        mock_res.session = mock_session

        with mock.patch.object(auth_route.supabase.auth, "sign_in_with_password", return_value=mock_res):
            resp = self.client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertEqual(data["access_token"], "mock_access_token_xyz")
            self.assertEqual(data["token_type"], "bearer")


if __name__ == "__main__":
    unittest.main(verbosity=2)
