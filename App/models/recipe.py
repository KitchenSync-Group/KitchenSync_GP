from sqlalchemy import Column, Integer, String, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app import db

class Recipe(db.Model):
    """Model for user-created recipes"""
    __tablename__ = 'recipes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(100), nullable=False)
    instructions = Column(Text, nullable=False)  # Stored as JSON string of step list
    cooking_time = Column(Integer, nullable=True)  # Minutes
    serving_size = Column(Integer, nullable=True)
    dietary_specs = Column(JSON, nullable=True)  # List of dietary preferences
    meal_type = Column(String(50), nullable=True)
    substitutions = Column(JSON, nullable=True)  # Dict of ingredient: [alternatives]
    
    # Relationships
    ingredients = relationship("RecipeIngredient", backref="recipe", cascade="all, delete-orphan")
    
    def __init__(self, user_id, title, instructions, cooking_time=None, 
                 serving_size=None, dietary_specs=None, meal_type=None, 
                 substitutions=None):
        self.user_id = user_id
        self.title = title
        self.instructions = instructions
        self.cooking_time = cooking_time
        self.serving_size = serving_size
        self.dietary_specs = dietary_specs or []
        self.meal_type = meal_type
        self.substitutions = substitutions or {}
    
    def to_dict(self):
        """Convert the recipe to a dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'ingredients': [ingredient.to_dict() for ingredient in self.ingredients],
            'instructions': self.instructions,
            'cooking_time': self.cooking_time,
            'serving_size': self.serving_size,
            'dietary_specs': self.dietary_specs,
            'meal_type': self.meal_type,
            'substitutions': self.substitutions
        }

class RecipeIngredient(db.Model):
    """Model for recipe ingredients"""
    __tablename__ = 'recipe_ingredients'
    
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    name = Column(String(100), nullable=False)
    quantity = Column(String(50), nullable=True)
    unit = Column(String(20), nullable=True)
    
    def __init__(self, recipe_id, name, quantity=None, unit=None):
        self.recipe_id = recipe_id
        self.name = name
        self.quantity = quantity
        self.unit = unit
    
    def to_dict(self):
        """Convert the recipe ingredient to a dictionary"""
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit
        }
