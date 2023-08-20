from fastapi import APIRouter, status
from httpx import AsyncClient


router = APIRouter(prefix="/foods", tags=["Foods"])
client = AsyncClient()

URL = "https://api.spoonacular.com/food/ingredients/search"


@router.get("/", status_code=status.HTTP_200_OK)
def get_foods():
    params = {
        "query": "banana",
        "number": 2,
        "sort": "calories",
        "sortDirection": "desc",
    }
    response = client.get(URL, params=params)
    print("response: ", response)
