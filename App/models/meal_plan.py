from datetime import date
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from app import db

class MealPlan(db.Model):
    """Model for meal planning"""
    __tablename__ = 'meal_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(String(50), nullable=False)
    recipe_id = Column(String(100), nullable=False)  # Can be external API ID or internal DB ID
    recipe_title = Column(String(200), nullable=False)
    notes = Column(Text, nullable=True)
    
    def __init__(self, user_id, date, meal_type, recipe_id, recipe_title, notes=""):
        self.user_id = user_id
        self.date = date
        self.meal_type = meal_type
        self.recipe_id = recipe_id
        self.recipe_title = recipe_title
        self.notes = notes
    
    def to_dict(self):
        """Convert the meal plan to a dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if isinstance(self.date, date) else self.date,
            'meal_type': self.meal_type,
            'recipe_id': self.recipe_id,
            'recipe_title': self.recipe_title,
            'notes': self.notes
        }