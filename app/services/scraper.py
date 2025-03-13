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


async def fetch_iiitr_about():
    """Scrapes the About IIIT Raichur page."""
    page = await browser.newPage()
    await page.setUserAgent(USER_AGENT)
    await page.goto("https://iiitr.ac.in/about", {"waitUntil": "networkidle2"})

    data = await page.evaluate('''
        () => {
            const aboutText = document.querySelector(".about_text")?.innerText.trim() || "Not Found";
            const aisheText = document.querySelector("body > section.about_part.section_padding > div:nth-child(3) > div > div > div > h4")?.innerText.trim() || "Not Found";
            const gazetteText = document.querySelector("body > section.about_part.section_padding > div:nth-child(4) > div > div > div > h4")?.innerText.trim() || "Not Found";
            const videoLink = document.querySelector("iframe")?.getAttribute("src") || "Not Found";
            const logoDownload = document.querySelector("a[href*='logo']")?.getAttribute("href") || "Not Found";
            const logoDesign = document.querySelector("a[href*='about/logo']")?.getAttribute("href") || "Not Found";

            return {
                about: aboutText,
                aishe_code: aisheText,
                gazette_notification: gazetteText,
                video_link: videoLink.startsWith("http") ? videoLink : "https://iiitr.ac.in" + videoLink,
                logo_download: logoDownload.startsWith("http") ? logoDownload : "https://iiitr.ac.in" + logoDownload,
                logo_design_credit: logoDesign.startsWith("http") ? logoDesign : "https://iiitr.ac.in" + logoDesign
            };
        }
    ''')

    await page.close()
    return data

async def fetch_iiitr_administration():
    """Generic function to scrape data from a given page."""
    page = await browser.newPage()
    await page.setUserAgent(USER_AGENT)
    await page.goto("https://iiitr.ac.in/administration", {"waitUntil": "networkidle2"})

    data = await page.evaluate('''
        () => {
            function getTextAfterHeading(headingText) {
                const headings = Array.from(document.querySelectorAll("h2, h3, h4"));
                for (let h of headings) {
                    if (h.innerText.trim().includes(headingText)) {
                        let nextElem = h.nextElementSibling;
                        let textContent = "";
                        while (nextElem && !["H2", "H3", "H4"].includes(nextElem.tagName)) {
                            textContent += nextElem.innerText.trim() + " ";
                            nextElem = nextElem.nextElementSibling;
                        }
                        return textContent.trim() || "Not Found";
                    }
                }
                return "Not Found";
            }

            return {
                title: document.title || "No Title",
                description: document.querySelector("meta[name='description']")?.content || "No Description",
                main_text: document.querySelector("p")?.innerText.trim() || "No Main Text",
                video_link: document.querySelector("iframe")?.getAttribute("src") || "Not Found",
                image: document.querySelector("img")?.getAttribute("src") || "Not Found",
                custom_data: getTextAfterHeading("Custom Section")  // Modify as needed
            };
        }
    ''')

    await page.close()
    return data

async def fetch_iiitr_administration():
    """Generic function to scrape data from a given page."""
    page = await browser.newPage()
    await page.setUserAgent(USER_AGENT)
    await page.goto("https://iiitr.ac.in/administration", {"waitUntil": "networkidle2"})

    data = await page.evaluate('''
        () => {
            let tables = document.querySelectorAll("#customers"); 
            let structuredData = {
                activeMembers: [],
                previousMembers: []
            };

            tables.forEach((table, index) => {
                let rows = table.querySelectorAll("tbody tr");
                let sectionKey = index === 0 ? "activeMembers" : "previousMembers"; // Determine section key

                rows.forEach((row, rowIndex) => {
                    if (rowIndex === 0) return; // Skip the header row

                    let cells = row.querySelectorAll("td");
                    if (cells.length === 3) {
                        structuredData[sectionKey].push({
                            role: cells[0].innerText.trim(),
                            memberName: cells[1].innerText.trim(),
                            email: cells[2].innerText.trim().replace("[at]", "@") // Convert email format
                        });
                    }
                });
            });

            return structuredData;
        }
    ''')

    await page.close()
    return data

