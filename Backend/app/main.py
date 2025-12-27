import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.app.routes import router 
from Backend.app.model_service import load_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Credit Score API")

origins = ["http://localhost:8080", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router)

@app.on_event("startup")
def startup_event():
    logger.info("🚀 Starting up...")
    load_model()
    logger.info("✅ Ready!")