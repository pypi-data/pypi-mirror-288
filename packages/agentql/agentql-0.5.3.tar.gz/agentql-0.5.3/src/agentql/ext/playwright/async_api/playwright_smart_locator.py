import logging
from typing import TYPE_CHECKING, Dict, Tuple, Union

from playwright.async_api import Page as _Page

from agentql import AccessibilityTreeError, QueryParser, trail_logger
from agentql._core._syntax.node import ContainerNode
from agentql._core._utils import minify_query
from agentql.async_api._agentql_service import query_agentql_server
from agentql.ext.playwright._driver_constants import (
    DEFAULT_INCLUDE_ARIA_HIDDEN,
    DEFAULT_QUERY_TIMEOUT_SECONDS,
    DEFAULT_WAIT_FOR_NETWORK_IDLE,
)
from agentql.ext.playwright._network_monitor import PageActivityMonitor
from agentql.ext.playwright._utils import post_process_accessibility_tree
from agentql.ext.playwright.async_api.response_proxy import AQLResponseProxy

from .._utils import post_process_accessibility_tree
from .playwright_driver_async import (
    Locator,
    add_event_listeners_for_page_monitor_shared,
    determine_load_state_shared,
    find_element_by_id,
    get_page_accessibility_tree,
    process_iframes,
    remove_event_listeners_for_page_monitor_shared,
)

log = logging.getLogger("agentql")


class Page(_Page):
    if TYPE_CHECKING:

        async def get_by_prompt(
            self,
            prompt: str,
            timeout: int = DEFAULT_QUERY_TIMEOUT_SECONDS,
            wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
            include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
        ) -> Union[Locator, None]:
            """Get an web element by AI.
            Parameters:
            -----------
            prompt (str): The natural language description of the element to locate.
            timeout (int) (optional): Timeout value in seconds for the connection with backend api service.
            wait_for_network_idle (bool) (optional): Whether to wait for the network to be idle before querying the page.
            include_aria_hidden (bool) (optional): Whether to include elements with aria-hidden attribute in the accessibility tree.

            Returns:
            --------
            [Playwright Locator](https://playwright.dev/python/docs/api/class-locator) | None: The located element.
            """

        async def query_elements(
            self,
            query: str,
            timeout: int = DEFAULT_QUERY_TIMEOUT_SECONDS,
            wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
            include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
        ) -> AQLResponseProxy:  # type: ignore 'None' warning
            """
            Query the web page tree for elements that match the AgentQL query.

            Parameters:
            ----------
            query (str): The AgentQL query in String format.
            timeout (int) (optional): Timeout value in seconds for the connection with backend api service.
            wait_for_network_idle (bool) (optional): Whether to wait for the network to be idle before querying the page.
            include_aria_hidden (bool) (optional): Whether to include elements with aria-hidden attribute in the accessibility tree.

            Returns:
            -------
            AQLResponseProxy: AgentQL Response (Elements that match the query) of AQLResponseProxy type.
            """

        async def query_data(
            self,
            query: str,
            timeout: int = DEFAULT_QUERY_TIMEOUT_SECONDS,
            wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
            include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
        ) -> Dict[str, str]:  # type: ignore 'None' warning
            """
            Query the web page tree for data, such as a block of texts or numbers.

            Parameters:
            ----------
            query (str): The AgentQL query in String format.
            timeout (int) (optional): Timeout value in seconds for the connection with backend api service.
            wait_for_network_idle (bool) (optional): Whether to wait for the network to be idle before querying the page.
            include_aria_hidden (bool) (optional): Whether to include elements with aria-hidden attribute in the accessibility tree.

            Returns:
            -------
            dict: AgentQL Response (Elements that match the query) in dictionary format.
            """

        async def wait_for_page_ready_state(
            self, wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE
        ):
            """Wait for the page to reach the "Page Ready" state (i.e. page has entered a relatively stable state and most main content is loaded).

            Parameters:
            -----------
            wait_for_network_idle (bool) (optional): This acts as a switch to determine whether to use default checking mechanism. If set to `False`, this method will only check for whether page has emitted `load` [event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) and provide a less costly checking mechanism for fast-loading pages.
            """


async def _get_by_prompt(
    self,
    prompt: str,
    timeout: int = DEFAULT_QUERY_TIMEOUT_SECONDS,
    wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
    include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
) -> Union[Locator, None]:
    query = f"""
{{
    page_element({prompt})
}}
"""
    response, _ = await _execute_query(
        self,
        query=query,
        timeout=timeout,
        include_aria_hidden=include_aria_hidden,
        wait_for_network_idle=wait_for_network_idle,
        is_data_query=False,
    )
    response_data = response.get("page_element")
    if not response_data:
        return None

    tf623_id = response_data.get("tf623_id")
    iframe_path = response_data.get("attributes", {}).get("iframe_path")
    web_element = find_element_by_id(page=self, tf623_id=tf623_id, iframe_path=iframe_path)

    return web_element


async def _query_elements(
    self,
    query: str,
    timeout: int = DEFAULT_QUERY_TIMEOUT_SECONDS,
    wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
    include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
) -> AQLResponseProxy:
    response, query_tree = await _execute_query(
        self,
        query=query,
        timeout=timeout,
        include_aria_hidden=include_aria_hidden,
        wait_for_network_idle=wait_for_network_idle,
        is_data_query=False,
    )
    return AQLResponseProxy(response, self, query_tree)


async def _query_data(
    self,
    query: str,
    timeout: int = DEFAULT_QUERY_TIMEOUT_SECONDS,
    wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE,
    include_aria_hidden: bool = DEFAULT_INCLUDE_ARIA_HIDDEN,
) -> Dict[str, str]:
    response, _ = await _execute_query(
        self,
        query=query,
        timeout=timeout,
        include_aria_hidden=include_aria_hidden,
        wait_for_network_idle=wait_for_network_idle,
        is_data_query=True,
    )
    return response


async def _execute_query(
    page: Page,
    query: str,
    timeout: int,
    wait_for_network_idle: bool,
    include_aria_hidden: bool,
    is_data_query: bool,
) -> Tuple[dict, ContainerNode]:
    trail_logger.add_event(f"Querying {minify_query(query)} on {page}")
    log.debug(f"Querying {'data' if is_data_query else 'elements'}: {query}")

    query_tree = QueryParser(query).parse()

    await page.wait_for_page_ready_state(wait_for_network_idle=wait_for_network_idle)

    try:
        accessibility_tree = await get_page_accessibility_tree(
            page, include_aria_hidden=include_aria_hidden
        )
        await process_iframes(page, accessibility_tree)
        post_process_accessibility_tree(accessibility_tree)

    except Exception as e:
        raise AccessibilityTreeError() from e

    response = await query_agentql_server(
        query, accessibility_tree, timeout, page.url, is_data_query
    )

    return response, query_tree


# pylint: disable=W0212
async def _wait_for_page_ready_state(
    self, wait_for_network_idle: bool = DEFAULT_WAIT_FOR_NETWORK_IDLE
):
    trail_logger.add_event(f"Waiting for {self} to reach 'Page Ready' state")

    if not self._page_monitor:
        self._page_monitor = PageActivityMonitor()
    else:
        # Reset the network monitor to clear the logs
        self._page_monitor.reset()

    # Add event listeners to track DOM changes and network activities
    await add_event_listeners_for_page_monitor_shared(self, self._page_monitor)

    # Wait for the page to reach the "Page Ready" state
    await determine_load_state_shared(
        page=self, monitor=self._page_monitor, wait_for_network_idle=wait_for_network_idle
    )

    # Remove the event listeners to prevent overwhelming the async event loop
    await remove_event_listeners_for_page_monitor_shared(self, self._page_monitor)

    trail_logger.add_event(f"Finished waiting for {self} to reach 'Page Ready' state")


# Add the get_by_ai method to the Page class
setattr(_Page, "get_by_prompt", _get_by_prompt)

setattr(_Page, "query_elements", _query_elements)

setattr(_Page, "query_data", _query_data)

setattr(_Page, "wait_for_page_ready_state", _wait_for_page_ready_state)

setattr(_Page, "_page_monitor", None)
