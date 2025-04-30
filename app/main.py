from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers.router import router as main_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


async def not_found(request, exc):
    return JSONResponse({"message":"Route Not Found"}, status_code=request.status_code)


@app.get("/")
def health():
    return {"message":"Welcome to local Pune Farmer Market Rates API"}

@app.get("/health")
def health():
    return {"message":"Health OK"}

app.include_router(main_router, prefix="/rates", tags=["Rates"])