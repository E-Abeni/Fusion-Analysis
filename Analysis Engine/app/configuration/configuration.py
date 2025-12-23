import shelve
from pathlib import Path
import sqlite3
import dbm.sqlite3
import functools

_original_sqlite_connect = sqlite3.connect

#Multithreaded sqlite to work with uvicorn
@functools.wraps(_original_sqlite_connect)
def thread_safe_sqlite_connect(*args, **kwargs):
    if 'check_same_thread' in kwargs:
        kwargs.pop('check_same_thread')

    kwargs['check_same_thread'] = False
    return _original_sqlite_connect(*args, **kwargs)

sqlite3.connect = thread_safe_sqlite_connect
dbm.sqlite3.sqlite3.connect = thread_safe_sqlite_connect

class Configuration:
    def __init__(self, config_path):
        self.config_path = config_path
        self._config = None   

    def _load_config(self):
        if self._config is None:
            self._config = shelve.open(self.config_path, writeback=True)

    def get(self, key, default=None):
        self._load_config()
        return self._config.get(key, default)

    def set(self, key, value):
        self._load_config()
        self._config[key] = value
        self._config.sync()

    def delete(self, key):
        self._load_config()
        if key in self._config:
            del self._config[key]
            self._config.sync()

    def close(self):
        if self._config is not None:
            self._config.close()
            self._config = None
            