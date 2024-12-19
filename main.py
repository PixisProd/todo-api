from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
from contextlib import asynccontextmanager
from authx.exceptions import MissingTokenError, JWTDecodeError
from routers import auth_router, account_router
from config import description_for_api, refresh_tables_on_startup
from database import create_tables, delete_tables, create_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    if refresh_tables_on_startup:
        delete_tables()
        create_tables()
        print("Tables cleared")
    print("Starting")
    yield
    print("Closing")


app = FastAPI(
    lifespan=lifespan,
    title="ToDo API 📝",
    version="0.1.0",
    description=description_for_api,
    
)
app.include_router(router=auth_router)
app.include_router(router=account_router)


@app.get("{path:path}", tags=["Docs 📄"], summary="Redirection from all unauthorized paths to docs")
async def root():
    return RedirectResponse(url="/docs")


@app.exception_handler(MissingTokenError)
async def missing_token_error_handler(_, __):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Access denied: Authorization required or expired. Please Log In", "success": False})


@app.exception_handler(JWTDecodeError)
async def jwt_decode_error_handler(_, __):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"msg": "Access denied: Authorization required or expired. Please Log In", "success": False})


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
    