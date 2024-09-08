from datetime import date
import os

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def get_gallery_page():
    load_dotenv()

    token = os.environ["NEXTCLOUD_KEY"]

    # Configuration
    nextcloud_url = "https://cloud.jepedersen.dk/apps/memories/thisday"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    playwright = sync_playwright().start()
    # Use playwright.chromium, playwright.firefox or playwright.webkit
    # Pass headless=False to launch() to see the browser UI
    browser = playwright.firefox.launch()
    page = browser.new_page(extra_http_headers=headers)
    page.goto(nextcloud_url)
    page.wait_for_load_state("networkidle")
    return playwright, browser, page


def _scroll_down(page, fraction):
    page.evaluate(
        f"""const e = document.querySelector("div.vue-recycle-scroller");
        e.scrollTop = e.scrollHeight / {fraction};"""
    )
    page.wait_for_load_state("networkidle")


def download_images(path):
    pl, browser, page = get_gallery_page()

    # Scroll to the bottom to load the entire page
    for i in range(1, 10):
        _scroll_down(page, 10.0 / i)

    # Click all selectors
    page.evaluate(
        """const selects = document.querySelectorAll("span.check-circle-icon.select");
            for (const select of selects) {
                select.click()}
        """
    )

    def on_download(download):
        print(f"Downloading {download.url} as {path}.zip")
        download.save_as(f"{path}.zip")

    page.on("download", on_download)

    # Open download dialog
    page.evaluate(
        """document.querySelector("div.memories-top-bar div.action-item button").click();"""
    )
    # Trigger download
    page.evaluate(
        """document.querySelector("div.v-popper__popper.action-item__popper button[aria-label='Download']").click();"""
    )
    try:
        page.locator("button[aria-label='Download']").click()
    except Exception as e:
        # TODO: Why does this timeout??
        print("Timeout, probably expected?")

    pl.stop()


if __name__ == "__main__":
    # Clear previous downloads
    os.system("find . -type d -name '*_images' -exec rm -r {} +")

    path = current_date = date.today()
    # Format the date in YYYY-mm-dd format
    formatted_date = current_date.strftime("%Y-%m-%d")

    # Download images
    download_images(formatted_date)

    # Unzip all files
    os.system(f"unzip -o {formatted_date}.zip -d {formatted_date}_images")

    # Remove the zip file
    os.remove(f"{formatted_date}.zip")

    # Create a list of images
    os.system(f"ls {formatted_date}_images > images.txt")
