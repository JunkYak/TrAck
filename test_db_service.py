import asyncio
import traceback
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.repositories.recipe import RecipeRepository
from app.repositories.food_item import FoodItemRepository
from app.services.recipe import RecipeService
from app.schemas.recipe import RecipeCreate, RecipeIngredientCreate
from app.models.food_item import FoodItem

async def test_db():
    async with AsyncSessionLocal() as session:
        # Check if chicken breast exists
        food_id = "d956a732-2e1b-4114-9a5b-42c276975973"
        food_stmt = select(FoodItem).where(FoodItem.id == food_id)
        food_res = await session.execute(food_stmt)
        if not food_res.scalars().first():
            print(f"ERROR: Food item {food_id} does not exist in DB!")
            return

        repo = RecipeRepository(session)
        food_repo = FoodItemRepository(session)
        service = RecipeService(repo, food_repo)

        dto = RecipeCreate(
            name="Test Recipe 2",
            ingredients=[
                RecipeIngredientCreate(food_item_id=food_id, quantity=200)
            ]
        )
        user_id = "00000000-0000-0000-0000-000000000001"
        
        try:
            recipe = await service.create_recipe(user_id=user_id, data=dto)
            print(f"Success! Recipe created: {recipe.id}")
            await session.commit()
        except Exception as e:
            print("Creation Failed with Exception:")
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_db())
