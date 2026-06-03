from fastapi import APIRouter
from fastapi.responses import JSONResponse
from domain.use_cases.health import HealthUseCase

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check():
    try:
        use_case = HealthUseCase()
        result = use_case.check()
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "database": "unreachable", "detail": str(e)},
        )
