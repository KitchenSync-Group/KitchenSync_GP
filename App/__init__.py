import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

logging.basicConfig(level=logging.DEBUG)

# Define the base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the Base class
db = SQLAlchemy(model_class=Base)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    
    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Initialize the database
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from app.models.user import User
        from app.models.meal_plan import MealPlan
        from app.models.pantry import PantryItem
        from app.models.recipe import Recipe, RecipeIngredient
        from app.models.shopping_list import ShoppingListItem
        
        # Create all database tables
        db.create_all()
        
        @login_manager.user_loader
        def load_user(user_id):
            # Change to use SQLAlchemy models
            from app.models.user import User
            return User.query.get(user_id)
    
    # Register blueprints
    from app.views.auth import auth_bp
    from app.views.pantry import pantry_bp
    from app.views.recipe import recipe_bp
    from app.views.shopping_list import shopping_list_bp
    from app.views.meal_plan import meal_plan_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(pantry_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(shopping_list_bp)
    app.register_blueprint(meal_plan_bp)
    
    # Register route for index
    from app.views.auth import index
    app.add_url_rule('/', 'index', index)
    
    return app