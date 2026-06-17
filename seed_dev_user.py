import asyncio
from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models.user import User

async def seed_dev_user():
    dev_user_id = "00000000-0000-0000-0000-000000000001"
    
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.id == dev_user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        
        if user:
            print(f"User {dev_user_id} already exists.")
        else:
            print(f"Creating user {dev_user_id}...")
            new_user = User(
                id=dev_user_id,
                google_id="dev_stub_google_id",
                email="dev@track.local",
                name="Local Developer",
                is_active=True
            )
            session.add(new_user)
            await session.commit()
            print("User created successfully.")
            
        # Verify
        count_stmt = select(User)
        result = await session.execute(count_stmt)
        count = len(result.scalars().all())
        print(f"Total users in DB: {count}")

if __name__ == "__main__":
    asyncio.run(seed_dev_user())
