import asyncio
import traceback
from app.database.session import AsyncSessionLocal
from app.models.user import User
from app.models.food_item import FoodItem
from app.models.recipe import Recipe, RecipeIngredient
from app.models.meal_template import MealTemplate, MealTemplateFood, MealTemplateRecipe
from sqlalchemy import text

async def test_deletes():
    async with AsyncSessionLocal() as session:
        user_id = "00000000-0000-0000-0000-000000000001"
        
        # Setup
        f1 = FoodItem(user_id=user_id, name="Temp Food 1", calories_per_unit=10, protein_per_unit=1, unit="g", source="MANUAL")
        f2 = FoodItem(user_id=user_id, name="Temp Food 2", calories_per_unit=20, protein_per_unit=2, unit="g", source="MANUAL")
        session.add_all([f1, f2])
        await session.flush()
        
        r1 = Recipe(user_id=user_id, name="Temp Recipe 1")
        session.add(r1)
        await session.flush()
        
        ri = RecipeIngredient(recipe_id=r1.id, food_item_id=f2.id, quantity=100)
        session.add(ri)
        
        t1 = MealTemplate(user_id=user_id, name="Temp Template 1")
        session.add(t1)
        await session.flush()
        
        tf1 = MealTemplateFood(meal_template_id=t1.id, food_item_id=f1.id, quantity=100)
        tr1 = MealTemplateRecipe(meal_template_id=t1.id, recipe_id=r1.id, multiplier=1.0)
        session.add_all([tf1, tr1])
        await session.commit()
        
        print(f"Setup complete. Food: {f1.id}, Recipe: {r1.id}, Template: {t1.id}")
        
        # Test 1: Delete MealTemplateFood
        try:
            print("--- Test 1: Deleting MealTemplateFood directly")
            await session.delete(tf1)
            await session.commit()
            print("SUCCESS: Deleted MealTemplateFood directly.")
        except Exception as e:
            await session.rollback()
            print(f"FAILED: {type(e).__name__} - {e}")
            
        # Re-add tf1
        tf1 = MealTemplateFood(meal_template_id=t1.id, food_item_id=f1.id, quantity=100)
        session.add(tf1)
        await session.commit()
        
        # Test 2: Delete Recipe
        try:
            print("--- Test 2: Deleting Recipe referenced by Template")
            # Refetch r1
            r1_ref = await session.get(Recipe, r1.id)
            await session.delete(r1_ref)
            await session.commit()
            print("SUCCESS: Deleted Recipe. Cascade worked.")
            
            # Verify tr1 is gone
            tr_check = await session.get(MealTemplateRecipe, tr1.id)
            print(f"MealTemplateRecipe after Recipe deletion: {tr_check}")
        except Exception as e:
            await session.rollback()
            print(f"FAILED: {type(e).__name__} - {e}")

        # Test 3: Delete Food
        try:
            print("--- Test 3: Deleting Food referenced by Template")
            f1_ref = await session.get(FoodItem, f1.id)
            await session.delete(f1_ref)
            await session.commit()
            print("SUCCESS: Deleted Food.")
        except Exception as e:
            await session.rollback()
            print(f"FAILED: {type(e).__name__} - {e}")
            
        # Cleanup
        t_ref = await session.get(MealTemplate, t1.id)
        if t_ref:
            await session.delete(t_ref)
        f_ref1 = await session.get(FoodItem, f1.id)
        if f_ref1:
            await session.delete(f_ref1)
        f_ref2 = await session.get(FoodItem, f2.id)
        if f_ref2:
            await session.delete(f_ref2)
        await session.commit()
        print("Cleanup done.")

if __name__ == "__main__":
    asyncio.run(test_deletes())
