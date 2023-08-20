from contextvars import ContextVar

BROWSER = ContextVar("browser")


def get_browser():
    return BROWSER.get()


async def create_browser(playwright):
    chromium = playwright.chromium
    new_browser = await chromium.launch()
    BROWSER.set(new_browser)


async def close_browser():
    browser = get_browser()
    if browser is not None:
        await browser.close()
        print("Browser closed")
    else:
        print("No browser to close")
