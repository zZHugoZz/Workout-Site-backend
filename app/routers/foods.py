from fastapi import APIRouter, status
from httpx import AsyncClient
from ..config import settings


router = APIRouter(prefix="/foods", tags=["Foods"])
client = AsyncClient()

URL = "https://api.spoonacular.com/food/ingredients/search"


@router.get("/", status_code=status.HTTP_200_OK)
async def get_foods():
    params = {
        "apiKey": settings.spoonacular_api_key,
        "query": "banana",
        "number": 2,
        "sort": "calories",
        "sortDirection": "desc",
    }
    response = await client.get(URL, params=params)
    # print("response: ", response.content)
    return response.json()
