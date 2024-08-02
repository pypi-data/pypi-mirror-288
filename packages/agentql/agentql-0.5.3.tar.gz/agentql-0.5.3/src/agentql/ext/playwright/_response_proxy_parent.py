import json
import logging
from typing import Union

from playwright.sync_api import Locator

from agentql import AttributeNotFoundError, ContainerNode, trail_logger

log = logging.getLogger("agentql")


class BaseAQLResponseProxy:
    _response_data: Union[dict, list]
    _query_tree_node: ContainerNode

    def __getattr__(self, name) -> Union[Locator, "BaseAQLResponseProxy"]:
        if self._response_data is None:
            raise AttributeError("Response data is None")
        if name not in self._response_data:
            raise AttributeNotFoundError(
                name, self._response_data, query_tree_node=self._query_tree_node
            )
        trail_logger.add_event(f"Resolving element {name}")
        return self._resolve_item(
            self._response_data[name], self._query_tree_node.get_child_by_name(name)
        )  # type: ignore # returned value could be None, but to make static checker happy we ignore it

    def __getitem__(self, index: int) -> Union[Locator, "BaseAQLResponseProxy"]:
        if not isinstance(self._response_data, list):
            raise ValueError("This node is not a list")
        return self._resolve_item(self._response_data[index], self._query_tree_node)  # type: ignore # returned value could be None, but to make static checker happy we ignore it

    def __len__(self):
        if self._response_data is None:
            return 0
        return len(self._response_data)

    def __str__(self):
        return json.dumps(self._response_data, indent=2)
