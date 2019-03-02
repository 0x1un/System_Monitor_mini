import psutil
from functools import reduce


class PresentMomentSystemResource:

    # 实现单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self.memory = psutil.virtual_memory()
        self.cpu = psutil.cpu_times()
        self.disk = psutil.disk_usage("/")

        self.mb = pow(1024, 2)
        self.gb = pow(1024, 3)

    def memory_usage(self):

        total = self.memory.total / self.gb
        used = self.memory.used / self.gb
        free = total - used
        percent = round(free / total, 2)
        buffers = self.memory.buffers / self.gb
        cached = self.memory.cached / self.gb
        total, used, free, buffers, cached = map(
            lambda x: round(x, 2), [total, used, free, buffers, cached])

        return {
            "total": total,
            "used": used,
            "free": free,
            "free_percent": percent,
            "buffers": buffers,
            "cached": cached
        }

    def cpu_usage(self):
        count = psutil.cpu_count(logical=False)
        logical_count = psutil.cpu_count()
        percent = psutil.cpu_percent(interval=1)
        return {
            "count": count,
            "logical_count": logical_count,
            "percent": percent
            }

    def disk_usage(self):
        total, used, free = map(lambda x: round(x / self.gb), self.disk[:3])
        percent = self.disk.percent
        return {
            "total": total,
            "used": used,
            "free": free,
            "free_percent": percent
        }

    def process_id(self, keywords=['python']):
        attrs = psutil.process_iter(attrs=['pid', 'name'])

        pid = [[p.info
                for p in attrs
                if keyword in p.info['name']]
               for keyword in keywords]
        pid_number = reduce(lambda x, y: x + y, [len(p) for p in pid])
        return {"pid": pid, "type_number": len(pid), "pid_number": pid_number}
