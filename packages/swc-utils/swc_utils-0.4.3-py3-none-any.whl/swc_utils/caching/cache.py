import sys
from time import time


class Cache:
    def __init__(self, initiator: type = dict, initiator_data: dict or list = None):
        self.__initiator = initiator
        self.__initiator_data = initiator_data
        self.__init_cache()
        self._updated = time()

    def __init_cache(self):
        self.__cache = self.__initiator(self.__initiator_data) if self.__initiator_data is not None else self.__initiator()

    def _set(self, key, value):
        self.__cache[key] = value
        self._updated = time()

    def _get(self, key):
        return self.__cache[key]

    def __setitem__(self, key, value):
        self._set(key, value)

    def __getitem__(self, key):
        return self._get(key)

    def __dir__(self):
        return dir(self.__cache)

    def __iter__(self):
        return iter(self.__cache)

    def __len__(self):
        return len(self.__cache)

    def __contains__(self, key):
        return key in self.__cache

    def __delitem__(self, key):
        del self.__cache[key]

    def serialize(self):
        return self.__cache

    def clear(self):
        self.__init_cache()
        self._updated = time()

    def clear_expired(self, expiration_time: int):
        if self._updated + expiration_time < time():
            self.clear()

    def inspect(self):
        return {
            "type": type(self.__cache).__name__,
            "initial_size": sys.getsizeof(self.__initiator_data),
            "length": len(self.__cache),
            "updated": self._updated,
            "size": self.size
        }

    @property
    def updated(self):
        return self._updated

    @property
    def size(self):
        return sys.getsizeof(self.__cache)

    # List-only methods

    def extend(self, data):
        if type(self.__cache) is not list:
            raise TypeError("Can't extend non-list cache")
        self.__cache.extend(data)
        self._updated = time()

    def sort(self, key=None, reverse=False):
        if type(self.__cache) is not list:
            raise TypeError("Can't sort non-list cache")
        self.__cache.sort(key=key, reverse=reverse)
        self._updated = time()
