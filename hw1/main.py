from fastapi import FastAPI, Response, status
from pydantic import BaseModel

# Constants

FIXED_DISCOUNT = 0.8
MIN_PRICE = 3.0
DISCOUNT = 'Discount'

# Models

class Item(BaseModel):
    name: str
    price: float
    count: int

def with_discount(item: Item):
    return Item(name=item.name + ' ({})'.format(DISCOUNT),
                price=item.price * FIXED_DISCOUNT,
                count=item.count)

def validate(item: Item, threshold=MIN_PRICE):
    return item.price * FIXED_DISCOUNT >= threshold

ITEMS = [Item(name='item {}'.format(i), price=i, count=i * 2) for i in range (10)]

# API

app = FastAPI()

@app.get("/item/{id}", status_code=status.HTTP_200_OK)
async def get_item(id: int, response: Response):
    if 0 <= id < len(ITEMS):
        return ITEMS[id]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

@app.post("/item", status_code=status.HTTP_200_OK)
async def post_item(item: Item, response: Response):
    if not validate(item):
        response.status_code = status.HTTP_400_BAD_REQUEST
    else:
        return with_discount(item)
