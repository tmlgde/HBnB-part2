from app import create_app
from app.config import DevelopmentConfig

app = create_app(DevelopmentConfig)  # 👈 on passe la classe de config

if __name__ == '__main__':
    app.run()
