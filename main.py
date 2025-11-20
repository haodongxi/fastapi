from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Optional
# Import the database connection
from database_connection import get_supabase_client
from datetime import datetime, timezone

app = FastAPI()

# 全局异常处理器 - 处理404未找到路由的情况
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # 专门处理404错误
    if exc.status_code == HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "error": {
                    "code": "NOT_FOUND",
                    "message": "请求的资源不存在",
                    "path": str(request.url.path)
                }
            },
        )
    # 处理其他HTTP异常
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
                "status_code": exc.status_code
            }
        },
    )

# 处理请求验证错误
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "请求参数验证失败",
                "details": exc.errors()
            }
        },
    )

# 处理所有其他未捕获的异常
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "服务器内部错误",
                "error_type": str(type(exc).__name__)
            }
        },
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/test-json")
async def test_json():
    return {
        "message": "This is a test JSON response",
        "data": {
            "id": 123,
            "name": "Test Item",
            "description": "A sample item for testing purposes"
        },
        "timestamp": "2023-01-01T00:00:00Z"
    }


# Example route showing proper usage of database connection
@app.get("/news")
async def get_news():
    """
    Example route demonstrating proper usage of database connection.
    This avoids the "query_data is not a known attribute of None" error
    by properly handling the database connection.
    """
    try:
        # Get the database client (this will never return None now)
        db_client = get_supabase_client()
        
        current_time = datetime.now(timezone.utc)  # Recommended: explicitly use UTC timezone
        db_client.insert_data({"created_at":current_time.isoformat(), "name": "Test Item"})

        # Query data safely
        news_data = db_client.query_data()
        
        return {
            "success": True,
            "data": news_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch news: {str(e)}"
        )


@app.get("/news/{news_id}")
async def get_news_by_id(news_id: int):
    """
    Example route demonstrating proper usage of database connection for querying by ID.
    """
    try:
        # Get the database client (this will never return None now)
        db_client = get_supabase_client()
        
        # Query data by ID safely
        news_data = db_client.query_data_id(news_id)
        
        if not news_data:
            raise HTTPException(
                status_code=404,
                detail=f"News item with ID {news_id} not found"
            )
            
        return {
            "success": True,
            "data": news_data
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch news: {str(e)}"
        )