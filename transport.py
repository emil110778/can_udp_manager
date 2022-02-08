import asyncio

class Transport:
    
    def __init__(self):
        self.main_loop = asyncio.get_event_loop()

    async def send_data(self, data):
        raise NotImplementedError
    
    async def listen_data(self):
        raise NotImplementedError

