from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse
from datetime import date

from v1.schemas.schemas import *
from utils.auth import *

from servicies.order_service import RecipeService, OrderService

router = APIRouter()


@router.get('/recipe')
async def get_all_recipes():
    try:
        recipes = RecipeService.get_all_recipes()
        return recipes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post('/recipe')
async def create_recipe(recipe_data: RecipeCreate):
    try:
        recipe = RecipeService.create_recipe(
            doctor_name=recipe_data.doctor_name,
            license_number=recipe_data.license_number,
            client_name=recipe_data.client_name,
            medicine_id=recipe_data.medicine_id,
            issue_date=recipe_data.issue_date
        )
        return recipe
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    
@router.get('/recipe/date')
async def get_recipe_by_date(min_date: date):
    try:
        recipes = RecipeService.get_recipes_by_date(min_date)
        return recipes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete('/recipe/{id}')
async def delete_recipe_by_id(id: int):
    try:
        success = RecipeService.delete_recipe(id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        return {"message": "Recipe deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get('/recipe/{id}')
async def get_recipe_info_by_id(id: int):
    try:
        recipe = RecipeService.get_recipe_by_id(id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe not found"
            )
        return recipe
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/')
async def get_all_orders(start_date: date):
    try:
        orders = OrderService.get_orders_after_date(start_date=start_date)
        return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    

@router.get('/summary')
async def get_orders_summary(start_date: date):
    try:
        orders = OrderService.get_order_summary_after_date(start_date=start_date)
        return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )