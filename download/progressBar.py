#!/usr/bin/env python3 
"""
作者：微微寒
链接：https://www.zhihu.com/question/41132103/answer/93438156
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
"""
class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep
 
    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        p = self.chunk_size * self.count
        if p > self.total: p = self.total
        _info = self.info % (self.title, self.status, p, self.unit, self.seq, self.total, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        p = self.chunk_size * self.count
        if p >= self.total:   
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)
 