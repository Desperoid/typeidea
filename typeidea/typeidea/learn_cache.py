import time
import functools


CACHE = {}
def cache_it(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = repr(*args, **kwargs)
        try:
            result = CACHE[key]
        except:
            result = func(*args, **kwargs)
            CACHE[key] = result
        return key
    return inner

@cache_it
def query(sql):
    try:
        result = CACHE[sql]
    except KeyError:
        time.sleep(1)
        result = f'execute {sql}'
        CACHE[sql] = result

    return result

if __name__ == '__main__':
    start = time.time()
    query('select * from blog_post')
    print(time.time() -start)

    start = time.time()
    query('select * from blog_post')
    print(time.time() - start)