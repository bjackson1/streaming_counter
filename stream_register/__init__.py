import threading
from stream_counter import stream_counter


class stream_register:
    def __init__(self):
        self.lock = threading.Lock()
        self.streams = {}

    def add(self, subscription_id, stream_id):
        self.lock.acquire()

        try:
            if not subscription_id in self.streams:
                self.streams[subscription_id] = stream_counter()
        finally:
            self.lock.release()

        self.streams[subscription_id].renew(stream_id, 90, 3)
