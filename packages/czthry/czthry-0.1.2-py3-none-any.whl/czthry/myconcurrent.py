import concurrent.futures
from typing import Callable, Optional

EachCallback = Callable[[int, any, Optional[Exception]], None] # 每个任务回调方法，参数1：数据索引，参数2：返回值，参数3：异常

class Concurrent(object):
    def __init__(self, action, data_list, max_workers=3, each_callback:EachCallback=None):
        '''
        :param action: 每个线程执行的函数
        :param data_list: 数据列表
        :param max_workers: 最大线程数
        :param each_callback: 每个任务回调方法
        '''
        self.action = action
        self.data_list = data_list
        self.max_workers = max_workers
        self.each_callback = each_callback


    def start(self):
        ''' 开始执行 '''
        total = len(self.data_list)
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.action, i, data, total):i for i, data in enumerate(self.data_list)}
            if callable(self.each_callback):
                for future in concurrent.futures.as_completed(futures):
                    index = futures[future]
                    try:
                        result = future.result()
                        self.each_callback(index, result, None)
                    except Exception as error:
                        self.each_callback(index, None, error)
    pass
