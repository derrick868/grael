from website import create_app, db
from website.models import Customer

app = create_app()  # Make sure this creates and initializes the Flask app

with app.app_context():  # Use the app context to interact with the database
    user_id = 1  # Replace with the user ID you want to update
    user = Customer.query.get(user_id)
    if user:
        user.status = 'admin'
        db.session.commit()
        print(f"User {user.username} is now an admin.")
        print(f"User {user.email} is now an admin.")
    else:
        print("User not found.")
