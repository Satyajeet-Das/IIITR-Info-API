import asyncio
from pyppeteer import launch
from app.config.settings import CHROME_PATH, USER_AGENT

browser = None  # Global browser instance

async def start_browser():
    """Launches a headless browser instance."""
    global browser
    if not browser:
        browser = await launch(executablePath=CHROME_PATH, headless=True, args=["--no-sandbox"])
    return browser

async def close_browser():
    """Closes the browser instance."""
    global browser
    if browser:
        await browser.close()
        browser = None

async def fetch_page_content(url):
    """Fetches news details from the given URL."""
    page = await browser.newPage()
    await page.setUserAgent(USER_AGENT)
    await page.goto(url)

    data = await page.evaluate('''
        () => {
            let content = Array.from(document.querySelectorAll("h5 p"))
                .map(el => el.innerText.trim())
                .join(" ");
            let links = Array.from(document.querySelectorAll("h5 a")).reduce((acc, el) => {
                acc[el.innerText.trim()] = el.href;
                return acc;
            }, {});
            return { content, links };
        }
    ''')

    await page.close()
    return data

async def fetch_updates():
    """Scrapes news updates from the homepage."""
    page = await browser.newPage()
    await page.setUserAgent(USER_AGENT)
    await page.goto('https://iiitr.ac.in/')

    updates = await page.evaluate('''
        () => Array.from(document.querySelectorAll(".index-news-cards")).map(el => ({
            image: el.querySelector("img")?.getAttribute("src") || null,
            title: el.querySelector("h3")?.innerText.trim() || null,
            date: el.querySelector("h5.text-muted")?.innerText.trim() || null,
            link: el.querySelector("a")?.getAttribute("href") || null
        }))
    ''')

    await page.close()
    return updates
