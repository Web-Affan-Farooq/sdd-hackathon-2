from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.database import create_db_and_tables
from app.routers import todos
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_db_and_tables()
    yield
    # Shutdown


app = FastAPI(
    title="Todo API",
    description="A simple todo application with user isolation and authentication",
    version="1.0.0",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Todo API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(todos.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["."]
    )