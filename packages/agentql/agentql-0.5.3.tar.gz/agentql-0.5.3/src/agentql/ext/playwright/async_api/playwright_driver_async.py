import asyncio
import logging
import random
import time
from typing import TYPE_CHECKING, Optional, Union

from playwright.async_api import BrowserContext, ElementHandle, Error, Frame, FrameLocator
from playwright.async_api import Locator as _Locator
from playwright.async_api import Page, StorageState, async_playwright
from playwright_stealth import StealthConfig, stealth_async

from agentql import QueryParser, trail_logger
from agentql._core._errors import (
    AccessibilityTreeError,
    AgentQLServerError,
    AttributeNotFoundError,
    ElementNotFoundError,
    NoOpenBrowserError,
    NoOpenPageError,
    OpenUrlError,
    PageMonitorNotInitializedError,
    UnableToClosePopupError,
)
from agentql._core._js_snippets.snippet_loader import load_js
from agentql._core._utils import ensure_url_scheme
from agentql.async_api import ScrollDirection, WebDriver
from agentql.async_api._agentql_service import query_agentql_server
from agentql.async_api._response_proxy import AQLResponseProxy

from .._driver_constants import (
    RENDERER,
    SLOWEST_WEBSITE_AVG_LOAD_TIME,
    USER_AGENT,
    VENDOR,
    WEBSITE_AVG_LOAD_TIME,
)
from .._driver_settings import ProxySettings, StealthModeConfig
from .._html_constants import HTML_ROLE_MAPPING
from .._network_monitor import PageActivityMonitor
from .._utils import merge_iframe_tree_into_page, post_process_accessibility_tree

CURRENT_TF_ID_ATTR = "current_tf_id"

log = logging.getLogger("agentql")


class Locator(_Locator):
    if TYPE_CHECKING:

        async def __call__(self, *args, **kwargs): ...
        def __getattr__(self, name) -> Union[AQLResponseProxy["Locator"], "Locator"]: ...
        def __getitem__(self, index: int) -> Union[AQLResponseProxy["Locator"], "Locator"]: ...
        def __len__(self) -> int: ...


class PlaywrightWebDriver(WebDriver[Locator, Page, BrowserContext]):
    """
    PlaywrightWebDriver is a web driver that builds on top of [Playwright framework](https://playwright.dev/python/). It is the default web driver used by AgentQL. Users could use PlaywrightWebDriver for browser / page related activities, such as scrolling, wait for page to load, and browse in stealth mode.
    """

    def __init__(self, headless=False, proxy: Optional[ProxySettings] = None) -> None:
        """
        Construct the PlaywrightWebDriver instance.

        Parameters:
        -----------
        headless (bool) (optional): Whether to start browser in headless mode. Headless browser will run in background while headful browser will run like a normal browser.
        proxy (dict) (optional): The proxy setting dictionary that includes server, username, and password as key.

        Returns:
        --------
        PlaywrightWebDriver: An instance of PlaywrightWebDriver.
        """
        self._playwright = None

        self._browser = None
        """The current browser. Only use this to close the browser session in the end."""

        self._context = None
        """The current browser context. Use this to open a new page"""

        self._original_html = None
        """The page's original HTML content, prior to any AgentQL modifications"""

        self._headless = headless
        """Whether to run browser in headless mode or not."""

        self._proxy = proxy

        self._page_monitor = None

        self._stealth_mode_config = None

    async def get_text_content(self, web_element: Locator) -> Optional[str]:
        """
        Gets the text content of the web element.

        Parameters:
        -----------

        web_element ([Playwright Locator](https://playwright.dev/python/docs/api/class-locator)): The web element represented by Playwright's Locator object.

        Returns:
        --------

        str: The text content of the web element.
        """
        return await web_element.text_content()

    @property
    def is_headless(self) -> bool:
        """Returns whether the browser is running in headless mode or not.

        Returns:
        --------
        bool: True if the browser is running in headless mode, False otherwise."""
        return self._headless

    def enable_stealth_mode(
        self,
        webgl_vendor: str = VENDOR,
        webgl_renderer: str = RENDERER,
        nav_user_agent: str = USER_AGENT,
    ):
        """Enable the stealth mode and set the stealth mode configuration.
        Ideally parameters values should match some real values to avoid detection.
        To get a realistic examples, you can use browser fingerprinting websites such as https://bot.sannysoft.com/ and https://pixelscan.net/

        Parameters:
        -----------
        webgl_vendor (str) (optional):
            The vendor of the GPU used by WebGL to render graphics, such as `Apple Inc.`. After setting this parameter, your browser will emit this vendor information.
        webgl_renderer (str) (optional):
            Identifies the specific GPU model or graphics rendering engine used by WebGL, such as `Apple M3`. After setting this parameter, your browser will emit this renderer information.
        nav_user_agent (str) (optional):
            Identifies the browser, its version, and the operating system, such as `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36`. After setting this parameter, your browser will send this user agent information to the website.
        """
        self._stealth_mode_config = StealthModeConfig(
            vendor=webgl_vendor, renderer=webgl_renderer, nav_user_agent=nav_user_agent
        )

    async def open_url(self, url: str, new_page: bool = False):
        """Open URL in the browser.

        Parameters:
        ----------
        url (str): The URL to open.
        new_page (bool): Whether to open the URL in a new tab in that tab. To navigate to a new url with the current tab, use Playwright Page object's [page.goto()](https://playwright.dev/python/docs/api/class-page#page-goto) method.
        """
        if not self._browser or not self._context:
            raise NoOpenBrowserError()
        if new_page or len(self._context.pages) == 0:
            await self._open_url(url)
        else:
            url = ensure_url_scheme(url)
            await self.current_page.goto(url, wait_until="domcontentloaded")

    @property
    def current_url(self) -> str:
        """Get the URL of the current page being processed by AgentQL.

        Returns:
        --------
        str: The URL of the current page.
        """
        return self.current_page.url

    @property
    def html(self) -> Optional[str]:
        """Returns the original HTML (i.e. without any AgentQL modifications) fetched from the most recently loaded page".

        Returns:
        --------
        dict: The HTML content of the web page in Dict format.
        """
        return self._original_html

    @property
    def current_page(self) -> Page:
        """Returns the [Playwright page object](https://playwright.dev/python/docs/api/class-page) that represents the current page. Users could do more fine grained interaction using this page object, such as navigating to a different url or take screenshot of the page.

        Returns:
        --------
        [Playwright Page](https://playwright.dev/python/docs/api/class-page): The current page.
        """
        if not self._context:
            raise NoOpenBrowserError()

        if len(self._context.pages) == 0:
            raise NoOpenPageError()

        return self._context.pages[-1]

    @property
    def browser(self) -> BrowserContext:
        """Returns the current browser being used.

        Returns:
        --------
        BrowserContext: The current browser object.
        """
        if not self._context:
            raise NoOpenBrowserError()
        return self._context

    async def open_html(self, html: str):
        """
        Opens a new page and loads the given HTML content.

        Parameters:
        -----------
        html (str): The HTML content to load in the page.
        """
        if not self._browser or not self._context:
            raise NoOpenBrowserError()
        page = await self._context.new_page()
        await page.set_content(html)

    @property
    async def accessibility_tree(self) -> dict:
        """Returns the up-to-date accessibility tree of the page.

        Returns:
        --------
        dict: The accessibility tree of the page in Dict format.
        """
        try:
            accessibility_tree = await get_page_accessibility_tree(self.current_page)
            await process_iframes(self.current_page, accessibility_tree)
            return accessibility_tree
        except Exception as e:
            raise AccessibilityTreeError() from e

    async def wait_for_page_ready_state(self, wait_for_network_idle: bool = True):
        """Wait for the page to reach the "Page Ready" state (i.e. page has entered a relatively stable state and most main content is loaded).

        Usage:
        -----
        ```py
        session = agentql.start_async_session(YOUTUBE_URL)

        # Scroll to bottom to trigger comments loading
        await session.driver.scroll_to_bottom()

        # Wait for comments to load before making a query
        await session.driver.wait_for_page_ready_state()
        await session.query(QUERY)
        ```

        Parameters:
        -----------
        wait_for_network_idle (bool) (optional): This acts as a switch to determine whether to use default chekcing mechanism. If set to `False`, this method will only check for whether page has emitted `load` [event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) and provide a less costly checking mechanism for fast-loading pages.
        """
        page = self.current_page

        trail_logger.add_event(f"Waiting for {page} to reach 'Page Ready' state")
        if not self._page_monitor:
            self._page_monitor = PageActivityMonitor()
        else:
            # Reset the network monitor to clear the logs
            self._page_monitor.reset()

        # Add event listeners to track DOM changes and network activities
        await self._add_event_listeners_for_page_monitor(page)

        # Wait for the page to reach the "Page Ready" state
        await self._determine_load_state(
            page, self._page_monitor, wait_for_network_idle=wait_for_network_idle
        )

        # Remove the event listeners to prevent overwhelming the async event loop
        await self._remove_event_listeners_for_page_monitor(page)

        trail_logger.add_event(f"Finished waiting for {page} to reach 'Page Ready' state")

    async def scroll_page(self, scroll_direction: ScrollDirection, pixels: int = 720):
        """Scrolls the page up or down by given pixels. By default, it will scroll 720 pixels.

        Parameters:
        -----------
        scroll_direction (ScrollDirection): An enumeration class that represents the direction in which a scroll action can occur. Currently, it has `UP` and `DOWN` member.
        pixels (int) (optional): The number of pixels to scroll. 720 by default.
        """
        await self.wait_for_page_ready_state()
        delta_y = pixels if scroll_direction == ScrollDirection.DOWN else -pixels
        await self.current_page.mouse.wheel(delta_x=0, delta_y=delta_y)

    async def scroll_to_bottom(self):
        """Scrolls to the bottom of the current page."""
        await self.wait_for_page_ready_state()
        height_information = await self.current_page.evaluate(load_js("get_scroll_info"))
        viewport_height, total_height, scroll_height = height_information
        while scroll_height < total_height:
            scroll_height = scroll_height + viewport_height
            await self.current_page.mouse.wheel(delta_x=0, delta_y=viewport_height)
            await asyncio.sleep(random.uniform(0.05, 0.1))

    async def scroll_to_top(self):
        """Scrolls to the top of the current page."""
        await self.wait_for_page_ready_state()
        height_information = await self.current_page.evaluate(load_js("get_scroll_info"))
        viewport_height, scroll_height = height_information[0], height_information[2]
        while scroll_height > 0:
            scroll_height = scroll_height - viewport_height
            await self.current_page.mouse.wheel(delta_x=0, delta_y=-viewport_height)
            await asyncio.sleep(random.uniform(0.05, 0.1))

    async def take_screenshot(self, path: str):
        """Takes a screenshot of the current page.

        Parameters:
        -----------
        path (str): The path to save the screenshot.
        """
        await self.current_page.screenshot(path=path, full_page=True)

    async def _close_popup(self, popup_tree: dict, page_url: str, timeout: int = 500):
        """Close the popup by querying AgentQL server for the close button and perform a click action with web driver.

        Parameters:
        -----------
        popup_tree (dict): The accessibility tree that has the popup node as the parent.
        page_url (str): The URL of the active page.
        timeout (int) (optional): The timeout value for the connection with AgentQL server service.
        """
        query = """
            {
                popup {
                    close_btn
                }
            }
        """
        parser = QueryParser(query)
        query_tree = parser.parse()
        try:
            response = await query_agentql_server(
                query, popup_tree, timeout=timeout, page_url=page_url
            )
            agentql_response = AQLResponseProxy(response, self, query_tree)
            await agentql_response.popup.close_btn.click()
        except (AgentQLServerError, AttributeNotFoundError) as e:
            raise UnableToClosePopupError() from e

    async def _get_user_auth_session(self) -> StorageState:
        """
        Returns the user authentication session that contains the login session state of current browser. User could pass this information when starting the session to preserve previous login state.

        Returns:
        --------
        dict: User auth session in Python dictionary format.
        """
        if not self._context:
            raise NoOpenBrowserError()
        return await self._context.storage_state()

    async def _prepare_accessibility_tree(
        self, lazy_load_pages_count: int = 3, include_aria_hidden: bool = True
    ) -> dict:
        """Prepare the AT by modifing the dom. It will return the accessibility tree after waiting for page to load and dom modification.

        Parameters:
        -----------
        lazy_load_pages_count: The number of times to scroll down and up the page.

        Returns:
        --------
        dict: AT of the page
        """
        self._original_html = await self.current_page.content()
        await self._page_scroll(pages=lazy_load_pages_count)

        try:
            accessibility_tree = await get_page_accessibility_tree(
                self.current_page, include_aria_hidden=include_aria_hidden
            )
            await process_iframes(self.current_page, accessibility_tree)
            post_process_accessibility_tree(accessibility_tree)
            return accessibility_tree

        except Exception as e:
            raise AccessibilityTreeError() from e

    def _locate_interactive_element(self, response_data: dict) -> Locator:
        """
        Locates an interactive element in the web page.

        Parameters:
        -----------

        response_data (dict): The data of the interactive element from the AgentQL response.

        Returns:
        --------

        [Playwright Locator](https://playwright.dev/python/docs/api/class-locator): The web element represented by Playwright's Locator object.
        """
        tf623_id = response_data.get("tf623_id")
        if not tf623_id:
            raise ElementNotFoundError(self.current_page.url, "tf623_id")

        iframe_path = response_data.get("attributes", {}).get("iframe_path")
        interactive_element = find_element_by_id(self.current_page, tf623_id, iframe_path)
        trail_logger.spy_on_object(interactive_element)
        return interactive_element

    async def _apply_stealth_mode_to_page(self, page: Page):
        """Applies stealth mode to the given page.

        Parameters:
        ----------
        page (Page): The page to which stealth mode will be applied.
        """
        # Only mask User Agent in headless mode to avoid detection for headless browsers
        mask_user_agent = self._headless

        if self._stealth_mode_config is not None:
            await stealth_async(
                page,
                config=StealthConfig(
                    vendor=self._stealth_mode_config["vendor"],
                    renderer=self._stealth_mode_config["renderer"],
                    # nav_user_agent will only take effect when navigator_user_agent parameter is True
                    nav_user_agent=self._stealth_mode_config["nav_user_agent"],
                    navigator_user_agent=mask_user_agent,
                ),
            )

    async def _open_url(self, url: str):
        """Opens a new page and navigates to the given URL. Initialize the storgage state if provided.

        Parameters:
        ----------
        url (str): The URL to navigate to.
        storgate_state_content (optional): The storage state with which user would like to initialize the browser.
        """

        url = ensure_url_scheme(url)

        if not self._browser or not self._context:
            raise NoOpenBrowserError()

        try:
            page = await self._context.new_page()
            if self._stealth_mode_config is not None:
                await self._apply_stealth_mode_to_page(page)
            await page.goto(url, wait_until="domcontentloaded")
        except Exception as e:
            raise OpenUrlError(url) from e

    async def _page_scroll(self, pages=3):
        """Scrolls the page down first and then up to load all contents on the page.

        Parameters:
        ----------
        pages (int): The number of pages to scroll down.
        """
        if pages < 1:
            return

        if self._stealth_mode_config is None:
            delta_y = 10000
            for _ in range(pages):
                await self.current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
                await asyncio.sleep(0.1)

            delta_y = -10000
            await asyncio.sleep(1)
            for _ in range(pages):
                await self.current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
                await asyncio.sleep(0.1)
        else:
            for _ in range(pages):
                await self.scroll_to_bottom()
                await asyncio.sleep(0.1)

            await asyncio.sleep(1)

            for _ in range(pages):
                await self.scroll_to_top()
                await asyncio.sleep(0.1)

    async def _start_browser(
        self,
        user_auth_session: Optional[StorageState] = None,
    ):
        """Starts a new browser session and set storage state (if there is any).

        Parameters:
        ----------
        user_session_extras (optional): the JSON object that holds user session information
        headless (bool): Whether to start the browser in headless mode.
        load_media (bool): Whether to load media (images, fonts, etc.) or not.
        """
        ignored_args = [
            "--enable-automation",
            "--disable-extensions",
        ]
        args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-blink-features=AutomationControlled",
        ]
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self._headless, proxy=self._proxy, args=args, ignore_default_args=ignored_args
        )
        self._context = await self._browser.new_context(
            user_agent=USER_AGENT, storage_state=user_auth_session
        )

    async def _stop_browser(self):
        """Closes the current browser session."""
        if self._context:
            await self._context.close()
            self._context = None
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

    async def _determine_load_state(
        self,
        page: Page,
        monitor: PageActivityMonitor,
        timeout_seconds: int = 14,
        wait_for_network_idle: bool = True,
    ):
        await determine_load_state_shared(page, monitor, timeout_seconds, wait_for_network_idle)

    async def _add_event_listeners_for_page_monitor(self, page: Page):
        await add_event_listeners_for_page_monitor_shared(page, self._page_monitor)

    async def _remove_event_listeners_for_page_monitor(self, page: Page):
        await remove_event_listeners_for_page_monitor_shared(page, self._page_monitor)


async def _set_iframe_path(context: Union[Page, Frame], iframe_path=None):
    """
    Sets the iframe path in the given context.

    Parameters:
    ----------
    context (Page | Frame): The context in which the DOM will be modified.
    iframe_path (str, optional): The path to the iframe. Defaults to None.
    """
    await context.evaluate(
        load_js("set_iframe_path"),
        {"iframe_path": iframe_path},
    )


async def _iframe_contains_doc_or_body(frame: Union[Frame, ElementHandle]) -> bool:
    """
    Checks if an iframe contains document or body.

    Parameters:
    ----------
    frame (Frame): The iframe to check.

    Returns:
    --------
    bool: True if iframes contains these elements, False otherwise.
    """
    frame_context = await frame.content_frame()

    if not frame_context:
        return True

    return await frame_context.evaluate(load_js("iframe_contains_doc_or_body"))


async def process_iframes(
    page: Page,
    page_accessibility_tree: dict,
    *,
    iframe_path: str = "",
    frame: Union[Frame, ElementHandle, None] = None,
):
    """
    Recursively retrieves the accessibility trees for all iframes in a page or frame.

    Parameters:
    ----------
    iframe_path (str): The path of the iframe in the frame hierarchy.
    frame (Frame): The frame object representing the current frame.
    page_accessibility_tree (dict): The accessibility tree of the page.
    """

    if frame is None:
        iframes = await page.query_selector_all("iframe")
    else:
        content_frame = await frame.content_frame()
        if not content_frame:
            return
        iframes = await content_frame.query_selector_all("iframe")

    for iframe in iframes:
        if not await _iframe_contains_doc_or_body(iframe):
            continue
        iframe_id = await iframe.get_attribute("tf623_id")
        iframe_path_to_send = ""
        if iframe_path:
            iframe_path_to_send = f"{iframe_path}."
        iframe_path_to_send = f"{iframe_path_to_send}{iframe_id}"
        iframe_accessibility_tree = await _get_frame_accessibility_tree(iframe, iframe_path_to_send)

        merge_iframe_tree_into_page(iframe_id, page_accessibility_tree, iframe_accessibility_tree)

        await process_iframes(
            page=page,
            iframe_path=iframe_path_to_send,
            frame=iframe,
            page_accessibility_tree=page_accessibility_tree,
        )


async def _get_frame_accessibility_tree(frame: Union[Frame, ElementHandle], iframe_path) -> dict:
    """
    Retrieves the accessibility tree for a given frame.

    Parameters:
    ----------
    frame (Frame): The frame for which to retrieve the accessibility tree.
    iframe_path: The path of the iframe within the frame.

    Returns:
    --------
    dict: The accessibility tree for the frame.
    """
    frame_context = await frame.content_frame()

    if not frame_context:
        return {}

    await _set_iframe_path(context=frame_context, iframe_path=iframe_path)
    accessibility_tree = await get_page_accessibility_tree(frame_context)

    return accessibility_tree


def _get_frame_context(page: Page, iframe_path: Optional[str] = None) -> Union[FrameLocator, Page]:
    """
    Returns the frame context for the given iframe path.

    Parameters:
    ----------
    iframe_path (str): The path of the iframe within the frame.

    Returns:
    --------
    Frame | Page: The frame context for the given iframe path.
    """
    if not iframe_path:
        return page

    iframe_path_list = iframe_path.split(".")
    frame_context = page
    for iframe_id in iframe_path_list:
        frame_context = frame_context.frame_locator(f"[tf623_id='{iframe_id}']")
    return frame_context


def find_element_by_id(page: Page, tf623_id: str, iframe_path: str = "") -> Locator:
    """
    Finds an element by its TF ID within a specified iframe.

    Parameters:
    ----------
    tf623_id (str): The generated tf id of the element to find.
    iframe_path (str): The path to the iframe containing the element.

    Returns:
    --------
    Locator: The located element.

    Raises:
    ------
    ElementNotFoundError: If the element with the specified TF ID is not found.
    """
    try:
        element_frame_context = _get_frame_context(page=page, iframe_path=iframe_path)
        return element_frame_context.locator(f"[tf623_id='{tf623_id}']")  # type: ignore
    except Exception as e:
        raise ElementNotFoundError(page.url, tf623_id) from e


async def get_page_accessibility_tree(
    context: Union[Page, Frame], include_aria_hidden: bool = True
) -> dict:
    """
    Retrieves the accessibility tree for the given page.

    Parameters:
    ----------
    context (Page | Frame): The context in which to retrieve the accessibility tree.

    Returns:
    --------
    dict: The accessibility tree for the page.
    """
    if isinstance(context, Frame):
        # Get the Playwright Page object from the Frame object
        page = context.page
    else:
        page = context

    # Get the underlying impl object of the Page object so that we could set the current tf id attribute directly on it.
    # pylint: disable=protected-access
    page = page._impl_obj

    current_tf_id = getattr(page, CURRENT_TF_ID_ATTR, 0)

    result = await context.evaluate(
        load_js("generate_accessibility_tree"),
        {
            "currentGlobalId": current_tf_id,
            "roleTagMap": HTML_ROLE_MAPPING,
            "processIFrames": False,
            "includeAriaHidden": include_aria_hidden,
        },
    )

    setattr(page, CURRENT_TF_ID_ATTR, result.get("lastUsedId"))

    return result.get("tree")


def locate_interactive_element(page: Page, response_data: dict) -> Locator:
    tf623_id = response_data.get("tf623_id")
    if not tf623_id:
        raise ElementNotFoundError(page.url, "tf623_id")
    iframe_path = response_data.get("attributes", {}).get("iframe_path")
    interactive_element = find_element_by_id(page=page, tf623_id=tf623_id, iframe_path=iframe_path)
    return interactive_element


async def add_event_listeners_for_page_monitor_shared(page: Page, monitor: PageActivityMonitor):
    if not monitor:
        raise PageMonitorNotInitializedError()

    try:
        page.on("request", monitor.track_network_request)
        page.on("requestfinished", monitor.track_network_response)
        page.on("requestfailed", monitor.track_network_response)
        page.on("load", monitor.track_load)
        await page.evaluate(load_js("add_dom_change_listener"))
    # If the page is navigating, the evaluate function will raise an error. In this case, we wait for the page to load.
    except Error:
        start_time = time.time()
        while True:
            if monitor.get_load_status() or time.time() - start_time > WEBSITE_AVG_LOAD_TIME:
                break
            await asyncio.sleep(0.2)


async def determine_load_state_shared(
    page: Page,
    monitor: PageActivityMonitor,
    timeout_seconds: float = SLOWEST_WEBSITE_AVG_LOAD_TIME,
    wait_for_network_idle: bool = True,
):
    if not monitor:
        raise PageMonitorNotInitializedError()

    if not wait_for_network_idle:
        await page.wait_for_load_state("load")
        trail_logger.add_event("Page ready: 'load' event catched.")
        return

    start_time = time.time()

    while True:
        try:
            last_updated_timestamp = await page.evaluate(load_js("get_last_dom_change"))
        # If the page is navigating, the evaluate function will raise an error. In this case, we wait for the page to load.
        except Error:
            while True:
                if monitor.get_load_status() or time.time() - start_time > WEBSITE_AVG_LOAD_TIME:
                    break
                await asyncio.sleep(0.2)
            # monitor.check_conditions() is expecting milliseconds
            last_updated_timestamp = time.time() * 1000

        if monitor.is_page_ready(last_active_dom_time=last_updated_timestamp):
            break

        if time.time() - start_time > timeout_seconds:
            trail_logger.add_event("Page ready: Timeout while waiting for page to settle.")
            break
        await asyncio.sleep(0.1)


async def remove_event_listeners_for_page_monitor_shared(page: Page, monitor: PageActivityMonitor):
    if not monitor:
        raise PageMonitorNotInitializedError()

    try:
        page.remove_listener("request", monitor.track_network_request)
        page.remove_listener("requestfinished", monitor.track_network_response)
        page.remove_listener("requestfailed", monitor.track_network_response)
        page.remove_listener("load", monitor.track_load)
        await page.evaluate(load_js("remove_dom_change_listener"))

    except Error:
        log.warning("Unable to remove event listeners for page monitor.")
