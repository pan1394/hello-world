#!/usr/bin/env python3 

class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s, %.1f%%"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep
        self.completed_size = 0
 
    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        rate = (self.completed_size / self.total) * 100  
        _info = self.info % (self.title, self.status, self.completed_size , self.unit, self.seq, self.total, self.unit, rate)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        #p = self.chunk_size * self.count
        self.completed_size += self.chunk_size
        if self.completed_size >= self.total:   
            end_str = '\n'
            self.completed_size = self.total
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)
 

    def calulate(self, count=1):
        self.count += count
        self.completed_size += self.chunk_size
        if self.completed_size >= self.total:    
            self.completed_size = self.total
            self.status = self.fin_status 

    def print(self):
        is_end = False
        end_str = "\r"
        if self.completed_size >= self.total:
            end_str = '\n'
            is_end = True
        print(self.__get_info(), end=end_str)
        return is_end