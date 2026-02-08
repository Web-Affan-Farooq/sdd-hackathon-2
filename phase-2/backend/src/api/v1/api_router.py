from fastapi import APIRouter
from . import environment, architecture, api_contract


# Create the main API router
api_router = APIRouter()

# Include individual routers
api_router.include_router(environment.router, prefix="/environments")
api_router.include_router(architecture.router, prefix="/architectures")
api_router.include_router(api_contract.router, prefix="/api-contracts")