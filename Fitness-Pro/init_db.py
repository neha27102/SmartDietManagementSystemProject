from app import create_app, db
from app.services.seed_service import seed_foods

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_foods()
    print("Fitness Pro database initialized and nutrition data seeded.")
