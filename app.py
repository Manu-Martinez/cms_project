from . import create_app, db
from app.static import views

app = create_app()

with app.app_context():
    db.create_all()  # Create the database tables

if __name__ == "__main__":
    app.run()