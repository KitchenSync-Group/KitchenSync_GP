import os
import requests
from app.models.recipe import Recipe, RecipeIngredient
from app.controllers.pantry_controller import pantry_controller
from app.default_config import RECIPE_API_ENDPOINT
from app import db
import json

class RecipeController:
    def __init__(self):
        self.api_key = os.environ.get("RECIPE_API_KEY", "")
        self.api_endpoint = RECIPE_API_ENDPOINT
    
    def search_recipes_by_ingredients(self, user_id, include_missing=True):
        """Search for recipes based on user's pantry ingredients"""
        ingredients = pantry_controller.get_ingredient_names(user_id)
        if not ingredients:
            return []
        
        # Format ingredients for API call
        ingredient_list = ','.join(ingredients)
        
        # Call external recipe API
        try:
            response = requests.get(
                f"{self.api_endpoint}/recipes/findByIngredients",
                params={
                    "apiKey": self.api_key,
                    "ingredients": ingredient_list,
                    "number": 10,
                    "ranking": 1,
                    "ignorePantry": False
                }
            )
            
            if response.status_code == 200:
                recipes = response.json()
                
                # Filter/mark missing ingredients if requested
                if not include_missing:
                    recipes = [recipe for recipe in recipes if not recipe.get('missedIngredientCount', 0)]
                
                return recipes
            else:
                # If API fails, return empty list
                return []
        except Exception as e:
            print(f"API Error: {e}")
            return []
    
    def get_recipe_details(self, recipe_id):
        """Get detailed information about a recipe from the API"""
        try:
            response = requests.get(
                f"{self.api_endpoint}/recipes/{recipe_id}/information",
                params={
                    "apiKey": self.api_key,
                    "includeNutrition": False
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def add_user_recipe(self, user_id, title, ingredients, instructions, 
                         cooking_time, serving_size, dietary_specs=None, 
                         meal_type=None, substitutions=None):
        """Add a user's custom recipe"""
        # Create recipe
        new_recipe = Recipe(
            user_id=user_id,
            title=title,
            instructions=json.dumps(instructions) if isinstance(instructions, list) else instructions,
            cooking_time=cooking_time,
            serving_size=serving_size,
            dietary_specs=dietary_specs or [],
            meal_type=meal_type,
            substitutions=substitutions or {}
        )
        
        db.session.add(new_recipe)
        db.session.flush()  # To get the new recipe ID
        
        # Add ingredients
        if isinstance(ingredients, list):
            for ingredient in ingredients:
                if isinstance(ingredient, dict):
                    recipe_ingredient = RecipeIngredient(
                        recipe_id=new_recipe.id,
                        name=ingredient.get('name', ''),
                        quantity=ingredient.get('quantity', ''),
                        unit=ingredient.get('unit', '')
                    )
                    db.session.add(recipe_ingredient)
        
        db.session.commit()
        return new_recipe.id
    
    def get_user_recipes(self, user_id):
        """Get all recipes created by a user"""
        recipes = Recipe.query.filter_by(user_id=user_id).all()
        return {str(recipe.id): recipe for recipe in recipes}
    
    def get_recipe_by_id(self, recipe_id):
        """Get a specific user recipe by ID"""
        return Recipe.query.get(recipe_id)
    
    def update_recipe(self, recipe_id, **kwargs):
        """Update a user recipe"""
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return False
        
        # Update recipe attributes
        for key, value in kwargs.items():
            if hasattr(recipe, key):
                # Special handling for JSON fields
                if key in ['instructions', 'dietary_specs', 'substitutions'] and isinstance(value, (list, dict)):
                    value = json.dumps(value)
                setattr(recipe, key, value)
        
        db.session.commit()
        return True
    
    def delete_recipe(self, recipe_id):
        """Delete a user recipe"""
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return True
        return False
    
    def filter_recipes_by_diet(self, recipes, dietary_preference):
        """Filter recipes by dietary preference"""
        filtered = []
        for recipe in recipes:
            # For API recipes
            if isinstance(recipe, dict) and 'diets' in recipe and dietary_preference.lower() in [d.lower() for d in recipe['diets']]:
                filtered.append(recipe)
            # For user recipes (ORM objects)
            elif hasattr(recipe, 'dietary_specs') and recipe.dietary_specs and dietary_preference.lower() in [d.lower() for d in recipe.dietary_specs]:
                filtered.append(recipe)
        return filtered
    
    def filter_recipes_by_meal_type(self, recipes, meal_type):
        """Filter recipes by meal type"""
        filtered = []
        for recipe in recipes:
            # For API recipes
            if isinstance(recipe, dict) and 'dishTypes' in recipe and meal_type.lower() in [d.lower() for d in recipe['dishTypes']]:
                filtered.append(recipe)
            # For user recipes (ORM objects)
            elif hasattr(recipe, 'meal_type') and recipe.meal_type and recipe.meal_type.lower() == meal_type.lower():
                filtered.append(recipe)
        return filtered

recipe_controller = RecipeController()