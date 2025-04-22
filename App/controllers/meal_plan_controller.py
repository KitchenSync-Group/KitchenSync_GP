from datetime import datetime
from app import db
from app.models.meal_plan import MealPlan

class MealPlanController:
    @staticmethod
    def get_user_meal_plans(user_id):
        """Get all meal plans for a user"""
        meal_plans = MealPlan.query.filter_by(user_id=user_id).all()
        return [plan.to_dict() for plan in meal_plans]
    
    @staticmethod
    def get_meal_plan(plan_id):
        """Get a specific meal plan by ID"""
        plan = MealPlan.query.get(plan_id)
        return plan.to_dict() if plan else None
    
    @staticmethod
    def add_meal_plan(user_id, date, meal_type, recipe_id, recipe_title, notes=""):
        """Add a meal plan for a specific date and meal type"""
        # First check if a meal plan already exists for this date and meal type
        existing = MealPlan.query.filter_by(
            user_id=user_id,
            date=date,
            meal_type=meal_type
        ).first()
        
        if existing:
            # Update the existing meal plan
            existing.recipe_id = recipe_id
            existing.recipe_title = recipe_title
            existing.notes = notes
            db.session.commit()
            return existing.id
        else:
            # Create a new meal plan
            new_plan = MealPlan(
                user_id=user_id,
                date=date,
                meal_type=meal_type,
                recipe_id=recipe_id,
                recipe_title=recipe_title,
                notes=notes
            )
            db.session.add(new_plan)
            db.session.commit()
            return new_plan.id
    
    @staticmethod
    def update_meal_plan(plan_id, meal_type=None, recipe_id=None, recipe_title=None, notes=None):
        """Update a meal plan"""
        plan = MealPlan.query.get(plan_id)
        if not plan:
            return False
        
        if meal_type:
            plan.meal_type = meal_type
        if recipe_id is not None:
            plan.recipe_id = recipe_id
        if recipe_title:
            plan.recipe_title = recipe_title
        if notes is not None:
            plan.notes = notes
        
        db.session.commit()
        return True
    
    @staticmethod
    def delete_meal_plan(plan_id):
        """Delete a meal plan"""
        plan = MealPlan.query.get(plan_id)
        if plan:
            db.session.delete(plan)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_plans_by_date_range(user_id, start_date, end_date):
        """Get meal plans within a date range"""
        plans = MealPlan.query.filter(
            MealPlan.user_id == user_id,
            MealPlan.date >= start_date,
            MealPlan.date <= end_date
        ).all()
        return [plan.to_dict() for plan in plans]
    
    @staticmethod
    def get_plans_by_date(user_id, date):
        """Get all meal plans for a specific date"""
        plans = MealPlan.query.filter_by(
            user_id=user_id,
            date=date
        ).all()
        return [plan.to_dict() for plan in plans]