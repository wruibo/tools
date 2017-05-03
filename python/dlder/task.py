'''
    task and task manager
'''
import threading

from util import md5
from log import logger
from lock import AutoLock


class Resp:
    '''
        response from downloader
    '''
    def __init__(self, code, msg, headers):
        self.code = code
        self.msg = msg
        self.headers = headers


class Task:
    '''
        download task
    '''
    DOWNLOADING = "downloading"
    WAITING = "waiting"
    COMPLETED = "completed"

    def __init__(self, url, path):
        self.url = url
        self.path = path

        self.status = Task.WAITING
        self.resp = None

        self.size_dlded = 0
        self.size_total = -1

    def file_path(self):
        return "%s/%s" % (self.path, md5(self.url))

    def set_resp(self, code, msg, headers):
        self.resp = Resp(code, msg, headers)

    def set_progress(self, new_dlded):
        self.size_dlded += new_dlded

    def set_completed(self):
        self.status = Task.COMPLETED
        if self.size_total == -1:
            self.size_total = self.size_dlded

    def set_downloading(self):
        self.status = Task.DOWNLOADING

    def is_waiting(self):
        return self.status == Task.WAITING

    def is_downloading(self):
        return self.status == Task.DOWNLOADING

    def is_completed(self):
        return self.status == Task.COMPLETED


class TaskMgr:
    '''
        task manager for manage tasks
    '''
    def __init__(self, save_path="./"):
        self.save_path = save_path

        self.pos = 0
        self.tasks = []
        self.lock = threading.Lock()

    def load_tasks(self):
        pass

    def add_task(self, url):
        with AutoLock(self.lock):
            logger.info("add download task for url: %s", url)
            self.tasks.append(Task(url, self.save_path))

    def next_task(self):
        with AutoLock(self.lock):
            logger.info("get next download task.")
            while self.pos<len(self.tasks) and not self.tasks[self.pos].is_waiting():
                self.pos += 1
            if self.pos == len(self.tasks):
                return None

            self.tasks[self.pos].set_downloading()

            return self.pos

    def get_task(self, pos):
        with AutoLock(self.lock):
            return self.tasks[pos]

    def get_tasks(self, start=0, end=None):
        with AutoLock(self.lock):
            logger.info("gets download task %d:%d", start, -1 if end is None else end)
            if end is None or end>len(self.tasks):
                end = len(self.tasks) - 1
            return self.tasks[start:end]

    def set_resp(self, pos, code, msg, headers):
        with AutoLock(self.lock):
            self.tasks[pos].set_resp(code, msg, headers)

    def set_progress(self, pos, new_dlded):
        with AutoLock(self.lock):
            self.tasks[pos].set_progress(new_dlded)

    def set_completed(self, pos):
        with AutoLock(self.lock):
            self.tasks[pos].set_completed()