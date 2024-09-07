from module.base.logger import logger

class GamePageUnknownError(Exception):
    def __init__(self):
        exit()

class RequestHumanTakeover(Exception):
    # Request human takeover
    # Alas is unable to handle such error, probably because of wrong settings.

    def __init__(self):
        exit()

class TaskEnd(Exception):
    def __init__(self, task):
        logger.warning(f"{task} ended.")

class ScriptError(Exception):
    # This is likely to be a mistake of developers, but sometimes a random issue
    def __init__(self):
        exit()

class GameStuckError(Exception):
    def __init__(self):
        exit()

class GameNotRunningError(Exception):
    def __init__(self):
        exit()

class GameTooManyClickError(Exception):
    def __init__(self):
        exit()
