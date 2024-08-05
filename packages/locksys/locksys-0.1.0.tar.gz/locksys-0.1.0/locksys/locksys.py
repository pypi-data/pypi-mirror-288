"""
Locksys: A Python library for securely retrieving API keys from 1Password vaults.

This module provides a simple interface to retrieve API keys and other sensitive
information from 1Password vaults using the 1Password Connect SDK.
"""

from onepasswordconnectsdk import new_client_from_environment
from functools import lru_cache
from typing import Optional

class Locksys:
    """
    A class for retrieving API keys from 1Password vaults.

    Attributes:
        vault (str): The name of the 1Password vault to use (default is "API").
        _item (Optional[str]): The name of the item to retrieve.
        _key (Optional[str]): The name of the key to retrieve from the item.
        result (Optional[str]): The retrieved value.
    """
    def __init__(self, vault: str = "API"):
        self.vault = vault
        self._item: Optional[str] = None
        self._key: Optional[str] = None
        self.result: Optional[str] = None

    def item(self, item_name: str) -> 'Locksys':
        """Set the item to retrieve from the 1Password vault."""
        self._item = item_name
        return self

    def key(self, key_name: str) -> 'Locksys':
        """Set the name of the key to retrieve from the item."""
        self._key = key_name
        return self

    @lru_cache(maxsize=None)
    def _get_client(self):
        """Cached method to get the 1Password client."""
        return new_client_from_environment()

    def results(self) -> str:
        """Retrieve an API key from a 1Password vault."""
        if not all((self._item, self._key)):
            raise ValueError("Both item and key must be set before getting the result.")

        try:
            client = self._get_client()
            item = client.get_item(self._item, self.vault)
            
            self.result = next((field.value for field in item.fields if field.label == self._key), None)
            
            if self.result is None:
                raise ValueError(f"Key '{self._key}' not found in item '{self._item}'")
            
            return self.result
        except Exception as e:
            raise Exception(f"1Password Connect Error: {e}") from e
