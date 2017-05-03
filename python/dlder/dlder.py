import time, urllib2, threading

from log import logger


class Downloader(threading.Thread):
    def __init__(self, taskmgr):
        threading.Thread.__init__(self)
        self.name = self.getName()
        self.taskmgr = taskmgr
        self.stop = False
        self.stopped = True

        self.idle_secs = 0

    def launch(self):
        self.stop = False
        self.start()
        self.stopped = False

        return self

    def stop(self):
        self.stop = True
        self.join()
        self.stopped = True

    def busy(self):
        MAX_IDLE_SECONDS = 120
        if self.idle_secs > MAX_IDLE_SECONDS:
            return True
        return  False

    def download(self, pos):
        task = self.taskmgr.get_task(pos)
        logger.info("%s: start downloading %s...", self.name, task.url)

        try:
            f = open(task.file_path(), 'wb')
            opener = urllib2.urlopen(task.url)
            self.taskmgr.set_resp(pos, opener.code, opener.msg, opener.headers)

            content = opener.read(16*1024)
            while content:
                f.write(content)
                self.taskmgr.set_progress(pos, len(content))
                content = opener.read(16*1024)

            opener.close()
            f.close()
        except urllib2.HTTPError, e:
            self.taskmgr.set_resp(pos, e.code, e.msg, e.hdrs)
            logger.error(e)
        finally:
            self.taskmgr.set_completed(pos)

        logger.info("%s: download completed. ", self.name)

    def run(self):
        SLEEP_SECONDS = 5
        while not self.stop:
            pos = self.taskmgr.next_task()
            if pos is not None:
                self.download(pos)
                self.idle_secs = 0
            else:
                time.sleep(SLEEP_SECONDS)
                self.idle_secs += SLEEP_SECONDS

class DownloaderMgr(threading.Thread):
    '''
        downloader manager
    '''
    def __init__(self, taskmgr, min=1, max=16):
        threading.Thread.__init__(self, name="thread-dldmgr")
        self.taskmgr = taskmgr

        self.dlder_min = min
        self.dlder_max = max
        self.stop = False
        self.stopped = True

        self.dldlers = []

    def launch(self):
        self.stop = False
        self.start()
        self.stopped = False
        return self

    def stop(self):
        self.stop = True
        self.join()
        self.stopped = True

    def schedule(self):
        logger.info("schedule downloaders...")
        dlder_num = len(self.dldlers)
        if dlder_num < self.dlder_min:
            while len(self.dldlers) < self.dlder_min:
                self.dldlers.append(Downloader(self.taskmgr).launch())
        else:
            decrease_num = dlder_num - self.dlder_min
            decreased_dlders = []
            for dlder in self.dldlers:
                if decrease_num > 0:
                    if not dlder.busy():
                        dlder.stop()
                        decreased_dlders.append(dlder)
                        decrease_num -= 1
                else:
                    break

            for decreased in decreased_dlders:
                self.dldlers.remove(dlder)
        logger.info("schedule downloaders completed.")

    def run(self):
        while not self.stop:
            self.schedule()
            time.sleep(5)

if __name__ == "__main__":
    from task import TaskMgr
    taskmgr = TaskMgr()
    taskmgr.add_task("http://60.206.107.20/sohu/v1/TmxGTmPmqKIXyS93q4WW8LcVD663R8blh81Wo6XWlm47fFoGRMNiNw.mp4?k=D56rMr&p=j9lvzSwUopkG0pwioSv30S1GopXWsUwIWFo7oB2svm12ZDeS0tvGRD6sWYNsfY1svmfCZMbVwmfVZD6HfYXswmeBNMvcNT1CvmNCNF2OWGyXWByXvm6AZDNXfY1swm1BqVPcgYeSoMAARDx&r=TmI20LscWOoUgt8ISCGXLa64fjLJ5JzHiFKXaDvaE3itfhQcv30cp5lSRjZJKODOfoIWFN4wmXAyB2HWF6HWJW45BABqtk3e4seqVyW8T9Xe6kveKsAhA4HqM14r&q=OpC3hW7IWGodRDbswmfCyY2sWhNHfJbOlG6tfOXsWG6S0F2OfFdXfJysfOoURD6tfOoUZDJ&cip=116.243.163.161")
    taskmgr.add_task("http://60.206.107.12/sohu/v1/TmwUo6IsWY6HbSfXhKwIaJ8tUJ4EHFO4w3lkiqu4kxytHrChWoIymcAr.mp4?k=Lc6AMK&p=j9lvzSwUopkG0pwioSv30S1GopXWsUwIWFo7oB2svm12ZDeS0tvGRD6sWYNsfY1svmfCZMbVwmfVZD6HfYXswmeBNMvcNT1CvmNCNF2OWGN4fhA4vm6AZDNXfY1swm1BqVPcgYeSoMAARDx&r=TmI20LscWOoUgt8IS3ktRYxjaD5tWjv9vBotCqU4C5TEwagkaj6o5jJjmOxj6ODOfoIWFN4wmXAyB2HWhNO5B6sfhcFoOdvPSAehScATEEI5lbS9aSXUICbFXUyYk&q=OpC7hW7IWGodRDbswmfCyY2sWhNHfJbOlG6tfOXsWG6S0F2OfFdXfJytfBoURD64WBoUZDJ&cip=116.243.163.161")
    taskmgr.add_task("http://60.206.107.10/sohu/v1/TmXUTmPUT3lH4HFMXkFHafILeMyv0TfmWmy4W8wHqM14wmfcymcAr.mp4?k=pm98er&p=j9lvzSwUopkG0pwioSv30S1GopXWsUwIWFo7oB2svm12ZDeS0tvGRD6sWYNsfY1svmfCZMbVwmfVZD6HfYXswmeBNMvcNT1CvmNCNF2OWGN4fhA4vm6AZDNXfY1swm1BqVPcgYeSoMAARDx&r=TmI20LscWOoUgt8IS37aas3JfqQECgmEUgoSWFHtA3hapFMsC5ZomjU9faLkEODOfoIWFN4wmXAyB2HWBNHWJNHM8yCup97DKyeq20ey2x7Nt0t0BesbJXUyYk&q=OpCihW7IWGodRDbswmfCyY2sWhNHfJbOlG6tfOXsWG6S0F2OfFdXfJytZhoURD64WBoUZDJ&cip=116.243.163.161")
    taskmgr.add_task("http://60.206.107.10/sohu/v1/TmXUTmPUT3lH4HFMXkFHafILeMyv0TfmWmy4W8wHqM14wmfcymcAr.mp4?k=pm98er&p=j9lvzSwUopkG0pwioSv30S1GopXWsUwIWFo7oB2svm12ZDeS0tvGRD6sWYNsfY1svmfCZMbVwmfVZD6HfYXswmeBNMvcNT1CvmNCNF2OWGN4fhA4vm6AZDNXfY1swm1BqVPcgYeSoMAARDx&r=TmI20LscWOoUgt8IS37aas3JfqQECgmEUgoSWFHtA3hapFMsC5ZomjU9faLkEODOfoIWFN4wmXAyB2HWBNHWJNHM8yCup97DKyeq20ey2x7Nt0t0BesbJXUyYk&q=OpCihW7IWGodRDbswmfCyY2sWhNHfJbOlG6tfOXsWG6S0F2OfFdXfJytZhoURD64WBoUZDJ&cip=116.243.163.161")
    taskmgr.add_task("http://60.206.107.13/sohu/v1/TmPm0EIsWhbHDVki0eKFPA0DZheND6XI9DzqUGitvXytHrChWoIymcAr.mp4?k=gRkyNp&p=j9lvzSwUopkG0pwioSv30S1GopXWsUwIWFo7oB2svm12ZDeS0tvGRD6sWYNsfY1svmfCZMbVwmfVZD6HfYXswmeBNMvcNT1CvmNCNF2OWGN4fhAtwm6AZDNXfY1swm1BqVPcgYeSoMAARDx&r=TmI20LscWOoUgt8IS3ikLJlsCDaSlJocfD6SL1GaRJi43au4lIG84dXPSobyOoCNLfcWFN4wmXAyB2HWJWXlB6sWFcRgSX2b8wLP2vXWeAWhmA3hByU0VXLlm47fw&q=OpC3hW7IWGodRDbswmfCyY2sWhNHfJbOlG6tfOXsWG6S0F2OfFdXfJytZhoURD64WBoUZDJ&cip=116.243.163.161")

    downloadmgr = DownloaderMgr(taskmgr).launch()

    time.sleep(1000)