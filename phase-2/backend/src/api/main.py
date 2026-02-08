from fastapi import FastAPI
from ..config.settings import settings
from ..api.v1.api_router import api_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Backend Development Framework API",
        description="API for managing backend development environments, architectures, and API contracts",
        version="1.0.0",
        openapi_tags=[
            {
                "name": "Environments",
                "description": "Operations related to development environments"
            },
            {
                "name": "Architectures", 
                "description": "Operations related to service architectures"
            },
            {
                "name": "ApiContracts",
                "description": "Operations related to API contracts"
            }
        ]
    )

    # Include API routes
    app.include_router(api_router, prefix="/v1")

    @app.get("/health")
    def health_check():
        """Health check endpoint to verify the application is running."""
        return {"status": "healthy", "environment": settings.environment}

    return app


# Create the main application instance
app = create_app()


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)