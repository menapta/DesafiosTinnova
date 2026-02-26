from fastapi import FastAPI, Request, status
from fastapi.concurrency import asynccontextmanager
from contextlib import asynccontextmanager 
import httpx
import uvicorn

from app.controllers import LoginController, VehiclesController

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.Dependencies import getCacheClient
cacheClient = getCacheClient()


async def fetch_and_cache_data():
    urls = [
        "https://economia.awesomeapi.com.br/json/last/USD-BRL",
        "https://api.frankfurter.app/latest?from=USD&to=BRL"
    ]
    
    async with httpx.AsyncClient() as client:
        for url in urls: 
            try:
                response = await client.get(url, timeout=5.0)
                response.raise_for_status()
                data = response.json()
                
                dollarValue = None

                if "USDBRL" in data:
                    dollarValue = data["USDBRL"].get("high")
                elif "rates" in data:
                    dollarValue = data["rates"].get("BRL")

                if dollarValue:
                    formattedValue = "{:.2f}".format(float(dollarValue))

                    val_bytes = formattedValue.encode('utf-8')
                    cacheClient.set("tinnova:dolar2real", val_bytes, ex=3600)
                    print(f"INFO: Cache populado: {dollarValue} via {url}")
                    return 

            except Exception as e:
                print(f"WARNING: Falha em {url}: {e}")
        
        cacheClient.set("tinnova:dolar2real", b"error") 
        print("ERROR: Todas as tentativas de popular o cache falharam.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await fetch_and_cache_data()
    yield

app = FastAPI(title="Desafio Tinnova API", lifespan=lifespan)

app.include_router(LoginController.router, prefix="/auth", tags=["Auth"])
app.include_router(VehiclesController.router)

@app.get("/")
def root():
    return {"status": "API rodando com FastAPI!", "docs": "/docs"}


@app.exception_handler(RequestValidationError)
async def validationExceptionHandler(request: Request, exc: RequestValidationError):
    errors = []
    
    for error in exc.errors():
        errors.append({
            "field": error["loc"][-1], 
            "message": "Invalid value" if error["type"] == "type_error" else "Missing field"
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