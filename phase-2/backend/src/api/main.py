from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from ..config.settings import settings
from ..api.v1.api_router import api_router
from ..services.monitoring import monitoring_service


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

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        """Middleware to record requests for monitoring."""
        monitoring_service.record_request()
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            monitoring_service.record_error()
            raise e

    @app.get("/health")
    def health_check():
        """Health check endpoint to verify the application is running."""
        health_status = monitoring_service.get_health_status()
        return {
            "status": health_status.status,
            "environment": settings.environment,
            "details": health_status.details
        }

    @app.get("/metrics")
    def metrics():
        """Metrics endpoint for monitoring."""
        return monitoring_service.get_performance_metrics()

    return app


# Create the main application instance
app = create_app()


# For running with uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)