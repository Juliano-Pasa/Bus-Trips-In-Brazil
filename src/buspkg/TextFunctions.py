from buspkg import ProjectConstants

import time


def GetCharacterStream(text, timeInterval=ProjectConstants.DEFAULT_CHARACTER_TIME_INTERVAL):
    for c in text:
        yield c
        time.sleep(timeInterval)