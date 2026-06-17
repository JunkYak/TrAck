import asyncio
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database.session import AsyncSessionLocal
from app.models.recipe import Recipe, RecipeIngredient
from app.models.food_item import FoodItem

async def cleanup_orphans():
    async with AsyncSessionLocal() as session:
        # 1. Find all RecipeIngredients
        stmt = select(RecipeIngredient).options(
            selectinload(RecipeIngredient.recipe),
            selectinload(RecipeIngredient.food_item)
        )
        result = await session.execute(stmt)
        ingredients = result.scalars().all()

        orphans = []
        for ing in ingredients:
            if ing.food_item is None:
                orphans.append(ing)
        
        if not orphans:
            print("No orphaned RecipeIngredients found.")
            return

        for orphan in orphans:
            print(f"Orphan found:")
            print(f"  Recipe name: {orphan.recipe.name if orphan.recipe else 'Unknown'}")
            print(f"  Recipe ID: {orphan.recipe_id}")
            print(f"  Ingredient ID: {orphan.id}")
            print(f"  Missing food_item_id: {orphan.food_item_id}")
            
            # Delete the orphaned ingredient
            await session.delete(orphan)
            print(f"  --> Deleted orphaned RecipeIngredient {orphan.id}")
            
            # Check if recipe is empty now
            recipe_stmt = select(Recipe).where(Recipe.id == orphan.recipe_id).options(selectinload(Recipe.ingredients))
            recipe_result = await session.execute(recipe_stmt)
            recipe = recipe_result.scalars().first()
            if recipe and len(recipe.ingredients) == 1: # The one we are about to commit deleting
                print(f"  --> Recipe '{recipe.name}' is now empty. Deleting recipe.")
                await session.delete(recipe)
                
        await session.commit()
        print(f"Cleanup complete. Removed {len(orphans)} orphans.")

if __name__ == "__main__":
    asyncio.run(cleanup_orphans())
