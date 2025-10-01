from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api_definitions.api_v1.api_router import api_router
import logging

# Configure Logging
log_filename = "api_operations.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


# Middleware for Logging Requests
@app.middleware("http")
async def log_user_requests(request: Request, call_next):
    # Always get user_id from headers, default to 'anonymous'
    user_id = request.headers.get("user_id", "ai")
    logging.info(f"User: {user_id} | Method: {request.method} | Path: {request.url.path}")
    response = await call_next(request)
    return response
 

# Global Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    user_id = request.headers.get("user_id")
    logging.error(f"User: {user_id} | Path: {request.url.path} | Unhandled Exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error_message": f"{str(exc)}"},
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    user_id = request.headers.get("user_id")
    logging.warning(f"User: {user_id} | Path: {request.url.path} | ValueError: {exc}")
    return JSONResponse(
        status_code=400,
        content={"error_message": f"{str(exc)}"},
    )
