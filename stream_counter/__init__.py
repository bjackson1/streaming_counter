from datetime import datetime, timedelta
import threading


class stream_counter:
    def __init__(self):
        self.streams = {}
        self.lock = threading.Lock()

    def renew(self, stream_id, renewal_period_seconds, max_concurrent_streams):
        self.lock.acquire()

        try:
            stream_ids = self.streams.copy().keys()

            for id in stream_ids:
                if self.streams[id] < datetime.utcnow():
                    del(self.streams[id])

            if stream_id in self.streams.keys() \
                    or len(self.streams) < max_concurrent_streams:
                self.streams[stream_id] = datetime.utcnow() + timedelta(seconds=renewal_period_seconds)

                return True

        finally:
            self.lock.release()

        return False
