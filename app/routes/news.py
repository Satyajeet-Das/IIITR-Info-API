from fastapi import APIRouter
from app.services.scraper import fetch_updates, fetch_page_content

router = APIRouter()

@router.get("/updates")
async def get_updates():
    """Fetch updates and scrape additional details for each news article."""
    updates = await fetch_updates()

    for news in updates:
        if news["link"]:
            details = await fetch_page_content(news["link"])
            news["content"] = details["content"]
            news["links"] = details["links"]

    return {"updates": updates}
