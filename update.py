from website import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(text('ALTER TABLE product ADD COLUMN category_id INTEGER;'))
        print("Column 'category_id' added successfully.")
