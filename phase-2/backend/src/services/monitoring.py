import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class HealthStatus:
    """Represents the health status of a service or component."""
    status: str  # 'healthy', 'degraded', 'unhealthy'
    message: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None


class MonitoringService:
    """
    Service for monitoring application health and performance metrics.
    """
    
    def __init__(self):
        self.start_time = time.time()
        self.requests_count = 0
        self.errors_count = 0
    
    def get_uptime(self) -> float:
        """Get the application uptime in seconds."""
        return time.time() - self.start_time
    
    def record_request(self):
        """Record an incoming request."""
        self.requests_count += 1
    
    def record_error(self):
        """Record an error occurrence."""
        self.errors_count += 1
    
    def get_health_status(self) -> HealthStatus:
        """Get the overall health status of the application."""
        uptime = self.get_uptime()
        
        # Simple health check based on error rate
        if self.requests_count > 0:
            error_rate = self.errors_count / self.requests_count
            if error_rate > 0.1:  # More than 10% errors
                status = "unhealthy"
                message = f"High error rate: {error_rate:.2%}"
            elif error_rate > 0.05:  # More than 5% errors
                status = "degraded"
                message = f"Elevated error rate: {error_rate:.2%}"
            else:
                status = "healthy"
                message = "Application is healthy"
        else:
            # No requests yet, but that's okay
            status = "healthy"
            message = "Application is running, no requests processed yet"
        
        details = {
            "uptime_seconds": round(uptime, 2),
            "total_requests": self.requests_count,
            "total_errors": self.errors_count,
            "error_rate": round(self.errors_count / max(1, self.requests_count), 4)
        }
        
        return HealthStatus(
            status=status,
            message=message,
            timestamp=datetime.utcnow(),
            details=details
        )
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance-related metrics."""
        return {
            "uptime_seconds": round(self.get_uptime(), 2),
            "requests_count": self.requests_count,
            "errors_count": self.errors_count,
            "error_rate": round(self.errors_count / max(1, self.requests_count), 4),
            "timestamp": datetime.utcnow().isoformat()
        }


# Global monitoring service instance
monitoring_service = MonitoringService()