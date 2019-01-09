from flask import Flask
from flask_jwt_extended import JWTManager
from app.database.db import database
from app.routes import routes
from app import app


# app=Flask(__name__)
routes.endpoints(app)
app.config['JWT_SECRET_KEY'] = 'nicks'
jwt=JWTManager(app)


@app.before_first_request
def admin():
    data = database()
    data.check_admin()











if __name__ == "__main__":
    app.run(debug=True)