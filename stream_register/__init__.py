import threading
from stream_counter import stream_counter


class stream_register:
    def __init__(self):
        self.lock = threading.Lock()
        self.streams = {}

    def renew(self, subscription_id, stream_id):
        try:
            if self.lock.acquire(timeout=3):
                if not subscription_id in self.streams:
                    self.streams[subscription_id] = stream_counter()

            else:
                # Assumes that if a timeout occurs locking the dict that it is better to fail open (i.e. allow the stream)

                # We can expect that timeouts should not occur here, so it would be best to log to file when this occurs
                #  and pick up in monitoring/alerting
                return True

        except:
            return True

        finally:
            self.lock.release()

        return self.streams[subscription_id].renew(stream_id, 90, 3)
