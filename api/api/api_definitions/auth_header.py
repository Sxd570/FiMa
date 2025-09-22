from fastapi.security import APIKeyHeader

Authorization = APIKeyHeader(name="Authorization", scheme_name="Authorization")