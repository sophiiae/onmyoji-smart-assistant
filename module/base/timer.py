import time

class Timer:
    def __init__(self, waiting_limit, retry_max=0):
        """
        Args:
            waiting_limit (int, float): Timer limit
            retry_max (int): Timer reach confirm retry max. Default to 0.
                When using a structure like this, must set a count.
                Otherwise it goes wrong, if screenshot time cost greater than limit.

                if self.appear(MAIN_CHECK):
                    if confirm_timer.reached():
                        pass
                else:
                    confirm_timer.reset()

                Also, It's a good idea to set `retry_max`, to make it more stable on slow computers.
                Expected speed is 0.35 second / screenshot.
        """
        self.waiting_limit = waiting_limit
        self.retry_max = retry_max
        self.started_time = 0
        self.retry_count = retry_max

    def start(self):
        if not self.started():
            self.started_time = time.time()
            self.retry_count = 0

        return self

    def started(self):
        return bool(self.started_time)

    def current_waiting_time(self):
        """
        Returns:
            float
        """
        if self.started():
            return time.time() - self.started_time
        else:
            return 0.

    def reached(self):
        """
        Returns:
            bool
        """
        self.retry_count += 1
        reached_waiting_limit = time.time() - self.started_time > self.waiting_limit
        return reached_waiting_limit and self.retry_count > self.retry_max

    def reset(self):
        self.started_time = time.time()
        self.retry_count = 0
        return self

    def clear(self):
        self.started_time = 0
        self.retry_count = self.retry_max
        return self

    def reached_and_reset(self):
        """
        Returns:
            bool:
        """
        if self.reached():
            self.reset()
            return True
        else:
            return False

    def wait(self):
        """
        Wait until timer reached.
        """
        diff = self.started_time + self.waiting_limit - time.time()
        if diff > 0:
            time.sleep(diff)

    def __str__(self):
        return f'Timer(waiting_limit={round(self.current_waiting_time(), 3)}/{self.waiting_limit}, count={self.retry_count}/{self.retry_max})'

    __repr__ = __str__
