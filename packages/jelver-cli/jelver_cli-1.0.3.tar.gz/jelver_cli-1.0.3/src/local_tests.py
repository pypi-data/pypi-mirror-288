""" File to allow running tests locally """

import asyncio
from uuid import uuid4

from enums import (
    BrowserType,
    CaseType
)
from utils.api import Api
from utils.playwright_utils import (
    create_browser,
    fetch_html_and_screenshots,
    goto_url_with_timeout
)



# How to run this code:
#   1. Determine if user wants to provide a browser
#   2. If so provide browser_type + use_existing_instance = True
#   3. Read resulting status from run_tests return or pass an update_status_function
class LocalTests:
    """
    Class to run tests locally
    """
    def __init__(self,
            url,     
            api_key,
            browser_type=None,     
            use_existing_instance=False,
            update_status_function=None):
        """ Initialize the LocalTests class """
        self.api = Api(api_key)
        self.url = url
        self.browser_type = browser_type 
        self.use_existing_instance = use_existing_instance
        self.update_status_function=update_status_function
        self.browser = None
        self.page = None
        self.validate_browser_type()

        

    def validate_browser_type(self):    
        """ Validate the browser type """
        if self.browser_type is None:
            self.browser_type = BrowserType.CHROMIUM.value
            return

    def run(self):
        """Run the workflow synchronously"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.run_tests_locally())

    async def run_tests_locally(self):
        """
        Run the E2E test workflow 
        """
        # pylint: disable=too-many-arguments
        job_id = str(uuid4())

        self.browser = None
        try:
            self.browser = await create_browser(
                browser_type=self.browser_type,
                use_existing_instance=self.use_existing_instance
            )
            context = await self.browser.new_context()
            self.page = await context.new_page()
            return await self.run_algorithm(job_id)

        finally:
            if self.browser:
                await self.browser.close()


    async def run_algorithm(self, job_id):
        # pylint: disable=too-many-arguments, too-many-locals
        """
        Run the overall testing algorithm.
        """
        cases = self.api.list_cases()
        testing_cases = cases['testingCases']

        for case in testing_cases:
            case_id, case_info, case_type = self.extract_case_details(case)

            # NOT UNDERSTANDING THIS
            # if case_type != CaseType.ROUTE.value:
                # raise ValueError(f'Invalid Case Type: {case_id} | {case_type}')

            page_url = f'{self.url.rstrip("/")}/{case_info.lstrip("/")}'
            self.page = await goto_url_with_timeout(self.page, page_url)
            html, screenshots = await fetch_html_and_screenshots(self.page)
            status = self.api.test_case(job_id, case_id, html, screenshots)

            if self.update_status_function:
                self.update_status_function(status)

        return status


    def extract_case_details(self, case):
        """
        Extract case details from the provided case
        """
        return case['caseId'], case['origin'], case['caseName']
