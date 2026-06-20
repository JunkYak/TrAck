import asyncio
import sys
import os

# Add root directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.session import AsyncSessionLocal
from sqlalchemy import text

DEV_TEST_USER_ID = "00000000-0000-0000-0000-000000000001"

async def migrate_dev_data(new_user_id: str):
    print(f"Starting migration from dev user ({DEV_TEST_USER_ID}) to new user ({new_user_id})...")
    
    async with AsyncSessionLocal() as session:
        # Check if the new user actually exists
        user_exists = await session.execute(text("SELECT 1 FROM users WHERE id = :user_id"), {"user_id": new_user_id})
        if not user_exists.scalar():
            print(f"Error: User with ID {new_user_id} does not exist in the database.")
            return

        tables_with_user_id = [
            "weight_logs",
            "measurement_sessions",
            "exercises",
            "exercise_logs",
            "recipes",
            "meal_templates",
            "daily_nutrition_logs",
            "cardio_sessions",
            "food_items"
        ]

        total_updated = 0
        for table in tables_with_user_id:
            try:
                result = await session.execute(
                    text(f"UPDATE {table} SET user_id = :new_id WHERE user_id = :old_id"),
                    {"new_id": new_user_id, "old_id": DEV_TEST_USER_ID}
                )
                updated_count = result.rowcount
                total_updated += updated_count
                print(f"Updated {updated_count} rows in {table}")
            except Exception as e:
                print(f"Error updating {table}: {e}")
        
        await session.commit()
        print(f"\nMigration complete. Total rows updated: {total_updated}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/migrate_dev_data.py <NEW_USER_UUID>")
        sys.exit(1)
        
    new_user_uuid = sys.argv[1]
    asyncio.run(migrate_dev_data(new_user_uuid))
