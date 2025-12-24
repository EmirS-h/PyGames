from typing import Dict, Any


class Globals:
    _items: Dict[str, Any] = {}

    @classmethod
    def set(cls, key: str, value: Any):
        """Sets a global value. Overwrites if it exists."""
        cls._items[key] = value

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Gets a global value. Returns None (or default) if missing."""
        return cls._items.get(key, default)

    @classmethod
    def remove(cls, key: str):
        if key in cls._items:
            del cls._items[key]
