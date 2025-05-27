
# /order/clients/{id}/recipes - Рецепты клиента
# /order/doctors/{id}/recipes - Рецепты врача

# /order - CRUD для заказов (Order)
# /order/{id}/items - Элементы заказа
# /order/by_date - Заказы за период

# /order/recipes - CRUD для рецептов (Recipe)
# /order/recipes/validate - Проверка валидности рецепта
# /order/recipes/{id}/order_items - Элементы заказа по рецепту

# /order/payment_types - Типы оплаты (TypePay)


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from api.v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()