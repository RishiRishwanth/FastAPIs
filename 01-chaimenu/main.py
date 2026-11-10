from http.client import HTTPException

from fastapi import FastAPI,Query
from models import MenuItem,MenuResponse
from data import menu_items

app =FastAPI(
    title= "Chai point menu API",
    description= "Read only menu API for kiosk displays and mobile app"
)

@app.get("/")
def root():
    return {"message": "Welcome to Chai point menu API"}


@app.get("/menu", response_model=MenuResponse)
def get_menu(category: str | None = Query(None, description = "Filter by chaim snack or combo")):
    """Get the menu items, optionally filtered by category"""
    if category:
        filtered = [item for item in menu_items if item["category"]==category.lower()]
        if not filtered:
            raise HTTPException(status_code=404,detail = f"No Item found in category:{category}")
        return MenuResponse(count = len(menu_items), items = menu_items)
    return MenuResponse(count = len(menu_items), items = menu_items)


@app.get("/menu/{item_id}",response_model=MenuItem)
def get_item(item_id: int ):
    for item in menu_items:
        if item["id"]==item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item not found with id: {item_id}")
