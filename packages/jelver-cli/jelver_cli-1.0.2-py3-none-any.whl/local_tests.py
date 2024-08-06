""" File to allow running tests locally """

from uuid import uuid4

from .enums import (
    BrowserType,
    CaseType
)
from .utils.api import Api
from .utils.playwright import (
    create_browser,
    fetch_html_and_screenshots,
    goto_url_with_timeout
)


# How to run this code:
#   1. Determine if user wants to provide a browser
#   2. If so provide browser_type + use_existing_instance = True
#   3. Read resulting status from run_tests return or pass an update_status_function
async def run_tests_locally(
        base_url,
        api_key,
        browser_type=BrowserType.CHROMIUM,
        use_existing_instance=False,
        update_status_function=None):
    """
    Run the E2E test workflow 
    """
    # pylint: disable=too-many-arguments
    api = Api(api_key)
    job_id = str(uuid4())

    browser = None
    try:
        browser, context = await create_browser(
            browser_type=browser_type,
            use_existing_instance=use_existing_instance
        )
        page = await context.new_page()
        return await run_algorithm(
            job_id,
            base_url,
            page,
            api,
            update_status_function=update_status_function
        )

    finally:
        if browser:
            await browser.close()


async def run_algorithm(
        job_id,
        base_url,
        page,
        api,
        update_status_function=None):
    # pylint: disable=too-many-arguments, too-many-locals
    """
    Run the overall testing algorithm.
    """
    cases = api.list_cases()
    testing_cases = cases['testingCases']

    for case in testing_cases:
        case_id, case_info, case_type = extract_case_details(case)

        if case_type != CaseType.ROUTE.value:
            raise ValueError(f'Invalid Case Type: {case_id} | {case_type}')

        page_url = f'{base_url.rstrip("/")}/{case_info.lstrip("/")}'
        page = await goto_url_with_timeout(page, page_url)
        html, screenshots = await fetch_html_and_screenshots(page)
        status = api.test_case(job_id, case_id, html, screenshots)

        if update_status_function:
            update_status_function(status)

    return status


def extract_case_details(case):
    """
    Extract case details from the provided case
    """
    return case['caseId'], case['caseInfo'], case['caseType']
