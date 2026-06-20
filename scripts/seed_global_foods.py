import asyncio
import os
import sys

# Add the project root to the python path so imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select

from app.database.session import engine, AsyncSessionLocal
from app.models.food_item import FoodItem

GLOBAL_FOODS = [
    {"name": "Egg", "calories": 70, "protein": 6, "unit": "count"},
    {"name": "Cheese Slice", "calories": 60, "protein": 3, "unit": "count"},
    {"name": "Chapati", "calories": 100, "protein": 3, "unit": "count"},
    {"name": "Aloo Paratha", "calories": 220, "protein": 6, "unit": "count"},
    {"name": "Gobi Paratha", "calories": 180, "protein": 5, "unit": "count"},
    {"name": "Poori", "calories": 90, "protein": 2, "unit": "count"},
    {"name": "Appam", "calories": 120, "protein": 2, "unit": "count"},
    {"name": "Idli", "calories": 60, "protein": 2, "unit": "count"},
    {"name": "Dosa", "calories": 130, "protein": 3, "unit": "count"},
    {"name": "Idiyappam", "calories": 55, "protein": 1.5, "unit": "count"},
    {"name": "Puttu", "calories": 180, "protein": 4, "unit": "count"},
    {"name": "Cooked White Rice", "calories": 1.3, "protein": 0.026, "unit": "g"},
    {"name": "Biryani Rice", "calories": 1.8, "protein": 0.04, "unit": "g"},
    {"name": "Pasta Cooked", "calories": 1.5, "protein": 0.05, "unit": "g"},
    {"name": "Poha", "calories": 3.7, "protein": 0.13, "unit": "g"},
    {"name": "Chicken Curry", "calories": 1.8, "protein": 0.22, "unit": "g"},
    {"name": "Chicken Fry", "calories": 2.4, "protein": 0.26, "unit": "g"},
    {"name": "Mutton Curry", "calories": 2.5, "protein": 0.22, "unit": "g"},
    {"name": "Prawns Curry", "calories": 1.4, "protein": 0.24, "unit": "g"},
    {"name": "Fish Curry", "calories": 1.5, "protein": 0.22, "unit": "g"},
    {"name": "Rohu Fish", "calories": 1.2, "protein": 0.20, "unit": "g"},
    {"name": "Mackerel Fish", "calories": 2.0, "protein": 0.22, "unit": "g"},
    {"name": "Aila Fish", "calories": 1.7, "protein": 0.22, "unit": "g"},
    {"name": "Roopchand Fish", "calories": 1.4, "protein": 0.21, "unit": "g"},
    {"name": "Prawns Pickle", "calories": 2.0, "protein": 0.25, "unit": "g"},
    {"name": "Paneer", "calories": 2.65, "protein": 0.18, "unit": "g"},
    {"name": "Curd", "calories": 0.6, "protein": 0.035, "unit": "g"},
    {"name": "Milk", "calories": 0.64, "protein": 0.032, "unit": "ml"},
    {"name": "Palak Dal", "calories": 0.9, "protein": 0.05, "unit": "ml"},
    {"name": "Sambar", "calories": 0.4, "protein": 0.015, "unit": "ml"},
    {"name": "Dal", "calories": 1.1, "protein": 0.06, "unit": "ml"},
    {"name": "Black Chana Cooked", "calories": 1.6, "protein": 0.09, "unit": "g"},
    {"name": "Banana", "calories": 105, "protein": 1.3, "unit": "count"},
    {"name": "Mango Piece", "calories": 5, "protein": 0.07, "unit": "count"},
    {"name": "Watermelon Piece", "calories": 3, "protein": 0.06, "unit": "count"},
    {"name": "Muskmelon Piece", "calories": 3, "protein": 0.07, "unit": "count"},
    {"name": "Papaya Piece", "calories": 4, "protein": 0.05, "unit": "count"},
    {"name": "Litchi", "calories": 7, "protein": 0.08, "unit": "count"},
    {"name": "Cherry", "calories": 5, "protein": 0.08, "unit": "count"},
    {"name": "Blueberry", "calories": 1, "protein": 0.01, "unit": "count"},
    {"name": "Apple Piece", "calories": 4, "protein": 0.02, "unit": "count"},
    {"name": "Almond", "calories": 7, "protein": 0.25, "unit": "count"},
    {"name": "Cashew", "calories": 9, "protein": 0.28, "unit": "count"},
    {"name": "Pistachio", "calories": 4, "protein": 0.15, "unit": "count"},
    {"name": "Walnut Half", "calories": 13, "protein": 0.3, "unit": "count"},
    {"name": "Raisin", "calories": 3, "protein": 0.03, "unit": "count"},
    {"name": "Date", "calories": 23, "protein": 0.2, "unit": "count"},
    {"name": "Oats", "calories": 3.8, "protein": 0.13, "unit": "g"},
    {"name": "Sugar", "calories": 4, "protein": 0, "unit": "g"},
    {"name": "Peanut Butter", "calories": 6, "protein": 0.25, "unit": "g"},
    {"name": "Soya Chunks Dry", "calories": 3.45, "protein": 0.52, "unit": "g"},
    {"name": "Coconut Chutney", "calories": 2.5, "protein": 0.02, "unit": "g"},
    {"name": "Onion Chutney", "calories": 1.4, "protein": 0.02, "unit": "g"},
    {"name": "Aloo Fry", "calories": 1.8, "protein": 0.02, "unit": "g"},
    {"name": "Bread Slice", "calories": 80, "protein": 3, "unit": "count"},
    {"name": "Rajma Curry", "calories": 1.3, "protein": 0.08, "unit": "g"},
    {"name": "Chole Curry", "calories": 1.6, "protein": 0.09, "unit": "g"},
    {"name": "Peanuts", "calories": 6, "protein": 0.26, "unit": "g"},
    {"name": "Orange Piece", "calories": 4, "protein": 0.08, "unit": "count"},
    {"name": "Guava Piece", "calories": 5, "protein": 0.2, "unit": "count"}
]

async def seed_global_foods():
    async with AsyncSessionLocal() as session:
        for food_data in GLOBAL_FOODS:
            # Check if global food exists
            stmt = select(FoodItem).where(
                FoodItem.name == food_data["name"],
                FoodItem.unit == food_data["unit"],
                FoodItem.user_id.is_(None)
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing:
                # Update macros if they drifted
                existing.calories_per_unit = food_data["calories"]
                existing.protein_per_unit = food_data["protein"]
                print(f"Updated global food: {food_data['name']}")
            else:
                new_food = FoodItem(
                    name=food_data["name"],
                    unit=food_data["unit"],
                    calories_per_unit=food_data["calories"],
                    protein_per_unit=food_data["protein"],
                    source="SYSTEM",
                    user_id=None
                )
                session.add(new_food)
                print(f"Created global food: {food_data['name']}")

        await session.commit()
        print("Global foods seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_global_foods())
