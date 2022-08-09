from datetime import datetime, timezone
import time


class TimeHandler:
    @staticmethod
    def get_standard_utc_time() -> str:
        return datetime.fromtimestamp(time.time(), timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
