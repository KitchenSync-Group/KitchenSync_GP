from app.models.recipe import Recipe, RecipeIngredient
from app.models.pantry import PantryItem
from app.database import db_session
import datetime
import requests
from flask import current_app
import logging

def get_user_recipes(user_id):
    """Get all custom recipes for a user"""
    return Recipe.query.filter_by(user_id=user_id, is_custom=True).all()

def get_recipe(recipe_id, user_id=None):
    """Get a specific recipe"""
    query = Recipe.query.filter_by(id=recipe_id)
    if user_id:
        # Only filter by user_id if looking for custom recipes
        query = query.filter_by(user_id=user_id, is_custom=True)
    return query.first()

def create_recipe(user_id, title, instructions, ingredients, description=None, 
                  preparation_time=None, cooking_time=None, servings=1, 
                  image_url=None, meal_types=None, dietary_preferences=None):
    """Create a new custom recipe"""
    # Create recipe
    recipe = Recipe(
        user_id=user_id,
        title=title,
        description=description,
        instructions=instructions,
        preparation_time=preparation_time,
        cooking_time=cooking_time,
        servings=servings,
        image_url=image_url,
        is_custom=True
    )
    
    db_session.add(recipe)
    db_session.flush()  # Flush to get the recipe ID
    
    # Add ingredients
    for ing in ingredients:
        ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            name=ing['name'],
            quantity=ing['quantity'],
            unit=ing.get('unit', ''),
            notes=ing.get('notes', None),
            is_optional=ing.get('is_optional', False)
        )
        db_session.add(ingredient)
    
    db_session.commit()
    return recipe

def update_recipe(recipe_id, user_id, **kwargs):
    """Update a custom recipe"""
    recipe = get_recipe(recipe_id, user_id)
    if not recipe or not recipe.is_custom:
        return None
    
    # Update recipe fields
    for key, value in kwargs.items():
        if key != 'ingredients' and hasattr(recipe, key):
            setattr(recipe, key, value)
    
    # Update ingredients if provided
    if 'ingredients' in kwargs:
        # Delete existing ingredients
        RecipeIngredient.query.filter_by(recipe_id=recipe.id).delete()
        
        # Add new ingredients
        for ing in kwargs['ingredients']:
            ingredient = RecipeIngredient(
                recipe_id=recipe.id,
                name=ing['name'],
                quantity=ing['quantity'],
                unit=ing.get('unit', ''),
                notes=ing.get('notes', None),
                is_optional=ing.get('is_optional', False)
            )
            db_session.add(ingredient)
    
    recipe.updated_at = datetime.datetime.utcnow()
    db_session.commit()
    
    return recipe

def delete_recipe(recipe_id, user_id):
    """Delete a custom recipe"""
    recipe = get_recipe(recipe_id, user_id)
    if not recipe or not recipe.is_custom:
        return False
    
    db_session.delete(recipe)
    db_session.commit()
    
    return True

def search_recipes_by_ingredients(ingredients, dietary_preferences=None, limit=10):
    """Search for recipes using the Spoonacular API based on ingredients"""
    api_key = current_app.config['SPOONACULAR_API_KEY']
    
    # Build the API request
    base_url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        'apiKey': api_key,
        'ingredients': ','.join(ingredients),
        'number': limit,
        'ranking': 2,  # Maximize used ingredients
        'ignorePantry': False
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        recipes = response.json()
        
        # Get recipe information for each result to include instructions and dietary info
        detailed_recipes = []
        for recipe in recipes:
            recipe_id = recipe['id']
            recipe_info = get_recipe_information(recipe_id)
            if recipe_info:
                # Filter by dietary preferences if specified
                if dietary_preferences:
                    if not matches_dietary_preferences(recipe_info, dietary_preferences):
                        continue
                detailed_recipes.append(recipe_info)
        
        return detailed_recipes
    
    except requests.RequestException as e:
        logging.error(f"Error fetching recipes from Spoonacular: {e}")
        return []

def get_recipe_information(recipe_id):
    """Get detailed information for a recipe from Spoonacular API"""
    api_key = current_app.config['SPOONACULAR_API_KEY']
    
    base_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        'apiKey': api_key,
        'includeNutrition': False
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e:
        logging.error(f"Error fetching recipe information from Spoonacular: {e}")
        return None

def matches_dietary_preferences(recipe, preferences):
    """Check if a recipe matches dietary preferences"""
    if 'vegan' in preferences and not recipe.get('vegan', False):
        return False
    if 'vegetarian' in preferences and not recipe.get('vegetarian', False):
        return False
    if 'gluten_free' in preferences and not recipe.get('glutenFree', False):
        return False
    if 'dairy_free' in preferences and not recipe.get('dairyFree', False):
        return False
    return True

def get_missing_ingredients(recipe, user_id):
    """Determine which ingredients are missing from a user's pantry"""
    pantry_items = PantryItem.query.filter_by(user_id=user_id).all()
    pantry_names = [item.name.lower() for item in pantry_items]
    
    missing = []
    
    # Handle API recipes
    if not isinstance(recipe, Recipe):
        for ingredient in recipe.get('extendedIngredients', []):
            if ingredient['name'].lower() not in pantry_names:
                missing.append({
                    'name': ingredient['name'],
                    'amount': ingredient.get('amount', 0),
                    'unit': ingredient.get('unit', '')
                })
        return missing
    
    # Handle custom recipes
    for ingredient in recipe.ingredients:
        if ingredient.name.lower() not in pantry_names:
            missing.append({
                'name': ingredient.name,
                'amount': ingredient.quantity,
                'unit': ingredient.unit
            })
    
    return missing

def save_api_recipe(user_id, api_recipe):
    """Save a recipe from the API to the user's collection"""
    # Check if recipe already exists
    existing = Recipe.query.filter_by(api_id=api_recipe['id'], is_custom=False).first()
    if existing:
        return existing
    
    # Create new recipe
    recipe = Recipe(
        user_id=user_id,
        title=api_recipe['title'],
        description=api_recipe.get('summary', ''),
        instructions=api_recipe.get('instructions', ''),
        preparation_time=api_recipe.get('preparationMinutes', 0),
        cooking_time=api_recipe.get('cookingMinutes', 0),
        servings=api_recipe.get('servings', 1),
        image_url=api_recipe.get('image', None),
        source_url=api_recipe.get('sourceUrl', None),
        is_custom=False,
        api_id=api_recipe['id']
    )
    
    db_session.add(recipe)
    db_session.flush()  # Flush to get the recipe ID
    
    # Add ingredients
    for ing in api_recipe.get('extendedIngredients', []):
        ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            name=ing['name'],
            quantity=ing.get('amount', 0),
            unit=ing.get('unit', ''),
            notes=None,
            is_optional=False
        )
        db_session.add(ingredient)
    
    db_session.commit()
    return recipe