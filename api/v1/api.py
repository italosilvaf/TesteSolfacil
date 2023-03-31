from fastapi import APIRouter
from api.v1.endpoints import partner, plant, last_partners, top_capacity_plants


api_router = APIRouter()

# Incluindo as endpoints de partner.py
api_router.include_router(
    partner.router, prefix='/partners', tags=["partners"])

# Incluindo as endpoints de plant.py
api_router.include_router(plant.router, prefix='/plants', tags=["plants"])

# Incluindo as endpoints de last_partners.py
api_router.include_router(last_partners.router,
                          prefix='/last-partners', tags=["last-partners"])

# Incluindo as endpoints de top_capacity_plants.py
api_router.include_router(top_capacity_plants.router,
                          prefix='/top-capacity-plants', tags=["top-capacity-plants"])
