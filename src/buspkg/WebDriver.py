import undetected_chromedriver as uc
import random
from itertools import cycle

class WebDriver (uc.Chrome):
    __userAgents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Trailer/93.3.8652.5",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.3",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0."
    ]

    def __init__(self, options="ProjectDefault"):
        self.__userAgentRotator = self.__GetUserAgentRotator()

        driverOptions = self.__GetOptions(options)
        super().__init__(driverOptions)

    def get(self, url):
        self.__UpdateAgent()
        super().get(url)

    def __GetOptions(self, options):
        if options == "ProjectDefault":
            driverOptions = uc.ChromeOptions()
            driverOptions.headless = True
            driverOptions.timeout = { 'script': 1800 }
            return driverOptions

        if options == None:
            return uc.ChromeOptions()

        return options
    
    def __GetUserAgentRotator(self):
        random.shuffle(self.__userAgents)
        return cycle(self.__userAgents)
    
    def __UpdateAgent(self):
        self.execute_cdp_cmd(
            'Network.setUserAgentOverride', {
                "userAgent": next(self.__userAgentRotator)
            }
        )