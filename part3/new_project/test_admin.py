python3 - <<'PY'
from app import create_app
from app.services import facade

app = create_app()
with app.app_context():
    if not facade.get_user_by_email("admin@example.com"):
        admin = facade.create_user({
            "email": "admin@example.com",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "User",
            "is_admin": True
        })
        print("✅ Admin créé :", admin.to_dict())
    else:
        print("Admin déjà présent")
