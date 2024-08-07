""" Utility functions for Playwright """

import math
import os

import platform
import asyncio
from io import BytesIO
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

from enums import BrowserType
from utils.jelver_exceptions import JelverBrowserException


def get_user_data_dir(browser_type):
    """
    Get the default user data directory for the specified browser type.
    :param browser_type: Type of browser.
    :return: Path to the user data directory.
    """
    # pylint: disable=too-many-branches, too-many-return-statements
    system = platform.system()
    home = Path.home()

    if browser_type == BrowserType.FIREFOX.value:
        if system == 'Windows':
            return home / 'AppData' / 'Roaming' / 'Mozilla' / 'Firefox' / 'Profiles'
        if system == 'Darwin':  # macOS
            return home / 'Library' / 'Application Support' / 'Firefox' / 'Profiles'
        if system == 'Linux':
            return home / '.mozilla' / 'firefox'

    if browser_type == BrowserType.CHROMIUM.value:
        if system == 'Windows':
            return home / 'AppData' / 'Local' / 'Google' / 'Chrome' / 'User Data'
        if system == 'Darwin':  # macOS
            return home / 'Library' / 'Application Support' / 'Google' / 'Chrome'
        if system == 'Linux':
            return home / '.config' / 'google-chrome'

    if browser_type == BrowserType.EDGE.value:
        if system == 'Windows':
            return home / 'AppData' / 'Local' / 'Microsoft' / 'Edge' / 'User Data'
        if system == 'Darwin':  # macOS
            return home / 'Library' / 'Application Support' / 'Microsoft Edge'
        if system == 'Linux':
            return home / '.config' / 'microsoft-edge'

    if browser_type in [BrowserType.WEBKIT.value, BrowserType.SAFARI.value]:
        if system == 'Windows':
            raise JelverBrowserException('WebKit/Safari is not supported on Windows.')
        if system == 'Darwin':  # macOS
            return home / 'Library' / 'Safari'
        if system == 'Linux':
            raise JelverBrowserException('WebKit/Safari is not supported on Linux.')

    raise JelverBrowserException(f'Unsupported browser type or platform: {browser_type}, {system}')


async def create_browser(
        browser_type=BrowserType.CHROMIUM.value,
        use_existing_instance=False,
        in_container=False):
    """
    Create a new browser instance or use an existing user data directory.
    """
    playwright = await async_playwright().start()

    if use_existing_instance:
        user_data_dir = get_user_data_dir(browser_type)

        if not os.path.exists(user_data_dir):
            raise JelverBrowserException(f'User browser data directory does not exist: {user_data_dir}')

        if browser_type == BrowserType.FIREFOX.value:
            return await playwright.firefox.launch_persistent_context(
                user_data_dir=user_data_dir
            )

        if browser_type in [BrowserType.CHROMIUM.value, BrowserType.EDGE.value]:
            return await playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir
            )

        if browser_type in [BrowserType.WEBKIT.value, BrowserType.SAFARI.value]:
            raise JelverBrowserException(f'Using existing sessions is not supported for {browser_type.value}.')
        raise JelverBrowserException(f'Unsupported browser type: {browser_type}')


    args = []
    if in_container:
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--single-process'
        ]

    if browser_type == BrowserType.FIREFOX.value:
        return await playwright.firefox.launch(args=args)

    if browser_type in [BrowserType.CHROMIUM.value, BrowserType.EDGE.value]:
        return await playwright.chromium.launch(args=args)

    if browser_type in [BrowserType.WEBKIT.value, BrowserType.SAFARI.value]:
        return await playwright.webkit.launch(args=args)
    raise JelverBrowserException(f"Unsupported browser type: {browser_type}")


async def goto_url_with_timeout(page, url, timeout_ms=5000):
    """
    Go to the page and do not wait longer than the timeout.
    """
    try:
        await asyncio.wait_for(
            page.goto(url, wait_until="networkidle"),
            timeout_ms / 1000
        )
    except asyncio.TimeoutError:
        pass
    return page


async def fetch_html_and_screenshots(
        page,
        max_page_size_bytes=1048576,
        max_num_screenshots=None):
    """
    Fetch the HTML and screenshots from the provided page.
    """
    html_task = fetch_page_content(page, max_page_size_bytes)
    screenshots_task = capture_screenshots(
        page,
        max_num_screenshots
    )

    html_result, screenshots_result = await asyncio.gather(
        html_task, screenshots_task
    )

    if isinstance(html_result, Exception):
        raise html_result

    if isinstance(screenshots_result, Exception):
        raise screenshots_result

    return html_result, screenshots_result


async def fetch_page_content(page, max_page_size_bytes):
    """
    Fetch the page content and ensure it does not exceed the max page size.
    """
    content = await page.content()
    if len(content.encode('utf-8')) > max_page_size_bytes:
        raise JelverBrowserException("Page size exceeds the maximum limit")
    return content


async def capture_screenshots(page, max_num_screenshots=4):
    """
    Capture screenshots of the entire page and convert them to Pillow Images.

    The max_num_screenshots is requires as some website have infinite scrolling.
    """
    # Get the dimensions of the viewport and the full page
    viewport_height = await page.evaluate('window.innerHeight')
    full_page_height = await page.evaluate('document.body.scrollHeight')

    screenshots = []
    num_screenshots = math.ceil(full_page_height / viewport_height)

    for i in range(num_screenshots):
        if max_num_screenshots and i > max_num_screenshots:
            break

        # Scroll to the correct position
        await page.evaluate(f'window.scrollTo(0, {i * viewport_height})')

        # Capture the screenshot
        screenshot_bytes = await page.screenshot()
        screenshots.append(Image.open(BytesIO(screenshot_bytes)))

    return screenshots
