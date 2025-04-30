from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routers.router import router as main_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # List of allowed origins
    allow_credentials=False,           # Allow cookies, authorization headers, etc.
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)


async def not_found(request, exc):
    return JSONResponse({"message":"Route Not Found"}, status_code=request.status_code)


@app.get("/")
def health():
    return {"message":"Welcome to local Pune Farmer Market Rates API"}

@app.get("/health")
def health():
    return {"message":"Health OK"}

app.include_router(main_router, prefix="/rates", tags=["Rates"])