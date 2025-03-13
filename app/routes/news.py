from fastapi import APIRouter
from app.services.scraper import fetch_updates, fetch_page_content, fetch_iiitr_about, fetch_iiitr_administration

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

@router.get("/about")
async def get_iiitr_about():
    """Fetches details about IIIT Raichur from the official website."""
    about = await fetch_iiitr_about()
    return {"about": about}

@router.get("/administration")
async def get_iiitr_administration():
    """Fetches details about the administration of IIIT Raichur."""
    administration = await fetch_iiitr_administration()
    return {"administration": administration}


