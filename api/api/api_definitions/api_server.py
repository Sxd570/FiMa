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
    user_id = request.headers.get("user_id", "ai")

    # Read and store the request body
    try:
        body_bytes = await request.body()
        body_str = body_bytes.decode("utf-8") if body_bytes else ""
    except Exception as e:
        body_str = f"[Error reading body: {e}]"

    logging.info(
        f"User: {user_id} | Method: {request.method} | Path: {request.url.path} | Payload: {body_str}"
    )

    # Recreate the request for downstream handlers
    async def receive():
        return {"type": "http.request", "body": body_bytes}

    request = Request(request.scope, receive=receive)

    # Process the request
    response = await call_next(request)

    # Capture response body
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    # Log the response content
    try:
        response_text = response_body.decode("utf-8")
    except Exception:
        response_text = str(response_body)

    logging.info(
        f"User: {user_id} | Path: {request.url.path} | Response Status: {response.status_code} | Response: {response_text}"
    )

    # Recreate the response with the original body
    from starlette.responses import Response
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )


 

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
