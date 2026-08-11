"""
Pydantic schemas used for API response validation and serialization.
Keeping schemas in their own module makes it easy to add more (e.g. Task
schemas) later without cluttering main.py.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for the GET /health endpoint."""
    status: str
    timestamp: str