"""Monitoring and health check endpoints."""

from datetime import datetime
from typing import Dict, Any
import psutil
import platform

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "consensuswatch-api",
        "version": "0.1.0"
    }


@router.get("/health/detailed")
async def detailed_health() -> Dict[str, Any]:
    """Detailed health check with system metrics."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "consensuswatch-api",
            "version": "0.1.0",
            "system": {
                "platform": platform.system(),
                "python_version": platform.python_version(),
                "cpu_percent": cpu_percent,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "percent_used": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "percent_used": disk.percent
                }
            }
        }
    except Exception as e:
        return {
            "status": "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.get("/metrics")
async def metrics() -> Dict[str, Any]:
    """Prometheus-style metrics endpoint."""
    memory = psutil.virtual_memory()

    return {
        "consensuswatch_memory_usage_bytes": memory.used,
        "consensuswatch_memory_total_bytes": memory.total,
        "consensuswatch_cpu_percent": psutil.cpu_percent(interval=1),
        "consensuswatch_uptime_seconds": int(datetime.utcnow().timestamp() - psutil.boot_time()),
    }


@router.get("/ready")
async def readiness_check() -> Dict[str, bool]:
    """Kubernetes-style readiness probe."""
    # Check if all dependencies are ready
    try:
        # Add checks for:
        # - Model loaded
        # - Redis connection
        # - Database connection
        # etc.

        return {"ready": True}
    except Exception:
        return {"ready": False}


@router.get("/live")
async def liveness_check() -> Dict[str, bool]:
    """Kubernetes-style liveness probe."""
    return {"alive": True}
