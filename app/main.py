from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.services.scraper import start_browser, close_browser
from app.routes.news import router as news_router
from app.routes.home import router as home_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages browser lifecycle: starts on app start and closes on shutdown."""
    await start_browser()
    try:
        yield
    finally:
        await close_browser()

app = FastAPI(lifespan=lifespan)

# Register Routes
app.include_router(home_router)
app.include_router(news_router)
