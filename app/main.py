from fastapi import FastAPI, Request, status
import uvicorn
from app.controllers import LoginController

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Desafio Tinnova API")

app.include_router(LoginController.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"status": "API rodando com FastAPI!", "docs": "/docs"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    
    for erro in exc.errors():
        errors.append({
            "field": erro["loc"][-1], 
            "message": "Invalid value" if erro["type"] == "type_error" else "Missing field"
        })
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "details": errors
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)