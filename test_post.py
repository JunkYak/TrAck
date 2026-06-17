import asyncio
import httpx

async def test_create_recipe():
    payload = {
        "name": "Test Recipe",
        "ingredients": [
            {
                "food_item_id": "d956a732-2e1b-4114-9a5b-42c276975973",
                "quantity": 200
            }
        ]
    }
    
    async with httpx.AsyncClient() as client:
        # Assuming the uvicorn server is running on localhost:8000
        # If it requires auth, get_current_user_id is returning the stub anyway.
        # But we need an auth header otherwise the HTTPBearer dependency might fail?
        # Actually `get_current_token_payload` raises 401 if token is missing.
        # Wait, the auth dependency might be checking for a token!
        # In dependencies.py:
        # _bearer = HTTPBearer(auto_error=False) ... 
        # But wait, we commented out get_current_user_id requiring the payload!
        # def get_current_user_id(): return _DEV_TEST_USER_ID
        response = await client.post('http://localhost:8000/api/v1/recipes', json=payload)
        
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(response.text)

if __name__ == "__main__":
    asyncio.run(test_create_recipe())
