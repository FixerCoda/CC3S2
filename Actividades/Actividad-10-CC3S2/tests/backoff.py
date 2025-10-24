import random
import time
from functools import wraps

def bounded_jitter_backoff(tries=3, base=0.05, cap=0.5):
    """Caped exponential backoff with jitter"""
    def deco(fn):
        @wraps(fn)
        def _wrap(*a, **kw):
            attempt = 0
            while True:
                try:
                    return fn(*a, **kw)
                except Exception as e:
                    attempt += 1
                    if attempt >= tries:
                        raise
                    sleep = min(cap, base * (2 ** (attempt - 1))) + random.uniform(0, base)
                    time.sleep(sleep)
        return _wrap
    return deco
