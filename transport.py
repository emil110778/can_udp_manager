import asyncio

class Transport:
    """Template class for transport module.
    Contine necessary function for module
    """
    async def send_data(self, data: bytes):
        """Asynchronous function for sending data

        Args:
            data (bytes): data encoded to byte array

        Raises:
            NotImplementedError: Will be overridden
        """
        raise NotImplementedError
    
    async def listen_data(self):
        """Asynchronous function for listening data

        Raises:
            NotImplementedError: Will be overridden
        """
        raise NotImplementedError

