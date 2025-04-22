from app.models.shopping_list import ShoppingListItem
from app.models.recipe import Recipe, RecipeIngredient
from app.database import db_session
import datetime

def get_user_shopping_list(user_id):
    """Get all shopping list items for a user"""
    return ShoppingListItem.query.filter_by(user_id=user_id).all()

def get_shopping_list_item(item_id, user_id=None):
    """Get a specific shopping list item"""
    query = ShoppingListItem.query.filter_by(id=item_id)
    if user_id:
        query = query.filter_by(user_id=user_id)
    return query.first()

def add_shopping_list_item(user_id, name, quantity=1, unit="", category=None, recipe_id=None):
    """Add a new item to the shopping list"""
    # Check if item already exists for this user
    existing_item = ShoppingListItem.query.filter_by(user_id=user_id, name=name, is_purchased=False).first()
    
    if existing_item:
        # Update quantity instead of creating new
        existing_item.quantity += quantity
        existing_item.updated_at = datetime.datetime.utcnow()
        db_session.commit()
        return existing_item
    
    # Create new item
    item = ShoppingListItem(
        user_id=user_id,
        name=name,
        quantity=quantity,
        unit=unit,
        category=category,
        recipe_id=recipe_id
    )
    
    db_session.add(item)
    db_session.commit()
    
    return item

def update_shopping_list_item(item_id, user_id, **kwargs):
    """Update a shopping list item"""
    item = get_shopping_list_item(item_id, user_id)
    if not item:
        return None
    
    # Update fields
    for key, value in kwargs.items():
        if hasattr(item, key):
            setattr(item, key, value)
    
    item.updated_at = datetime.datetime.utcnow()
    db_session.commit()
    
    return item

def delete_shopping_list_item(item_id, user_id):
    """Delete a shopping list item"""
    item = get_shopping_list_item(item_id, user_id)
    if not item:
        return False
    
    db_session.delete(item)
    db_session.commit()
    
    return True

def mark_item_as_purchased(item_id, user_id):
    """Mark a shopping list item as purchased"""
    return update_shopping_list_item(item_id, user_id, is_purchased=True)

def add_recipe_ingredients_to_shopping_list(user_id, recipe_id):
    """Add all ingredients from a recipe to the shopping list"""
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return False, "Recipe not found"
    
    for ingredient in recipe.ingredients:
        add_shopping_list_item(
            user_id=user_id,
            name=ingredient.name,
            quantity=ingredient.quantity,
            unit=ingredient.unit,
            recipe_id=recipe_id
        )
    
    return True, "Ingredients added to shopping list"

def clear_purchased_items(user_id):
    """Remove all purchased items from the shopping list"""
    items = ShoppingListItem.query.filter_by(user_id=user_id, is_purchased=True).all()
    
    for item in items:
        db_session.delete(item)
    
    db_session.commit()
    return len(items)