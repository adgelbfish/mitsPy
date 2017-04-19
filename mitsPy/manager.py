from mitsPy.mitsubishicontroller import MitsubishiController
import asyncio

class Manager:
    def __init__(self, controller_url, path="/servlet/MIMEReceiveServlet", loop = asyncio.get_event_loop()):
        self.controller = MitsubishiController(url=controller_url, path=path, loop=loop)
        self.initialize = self.controller.initialize
        self.groups = self.controller.groups
