class GamePageUnknownError(Exception):
    pass

class RequestHumanTakeover(Exception):
    # Request human takeover
    # Alas is unable to handle such error, probably because of wrong settings.
    pass

class TaskEnd(Exception):
    pass

class ScriptError(Exception):
    # This is likely to be a mistake of developers, but sometimes a random issue
    pass
