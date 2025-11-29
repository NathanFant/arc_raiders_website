from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth

app = FastAPI(
    title="Arc Raiders Loadout API",
    description="API for creating and sharing Arc Raiders loadouts",
    version="1.0.0",
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incude routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


# Health check endpoints
@app.get("/")
async def root():
    return {"message": "Arc Raiders API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "not connected yet"}


@app.get("/api/v1/test")
async def test_endpoint():
    return {"message": "API v1 is working!"}
