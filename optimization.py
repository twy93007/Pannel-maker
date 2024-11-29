from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

@lru_cache(maxsize=128)
def process_data(data):
    """处理数据的函数"""
    pass

def process_in_parallel(data_list):
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_data, data_list) 