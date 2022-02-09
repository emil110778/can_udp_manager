import asyncio
import socket
import struct

from anyio import create_udp_socket, create_connected_udp_socket

from transport import Transport

class Udp_socket(Transport):
    def __init__(self, local_port: int = 2000, 
                remote_host: str = 'localhost', 
                remote_port: int = 2001):
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port


    async def send_data(self, data: bytes):
        try:
            async with await create_connected_udp_socket(family = socket.AF_INET, 
                                                        remote_host = self.remote_host, 
                                                        remote_port = self.remote_port, 
                                                        local_host = 'localhost',
                                                        local_port = self.local_port - 1) as udp:

                await udp.send(bytes(data))
        except:
            print("can't send to host {}:{}".format(self.remote_host, self.remote_port))
        

    async def listen_data(self):
        try:
            async with await create_udp_socket(family = socket.AF_INET, local_port = self.local_port, local_host = 'localhost') as udp:
                async for packet, _ in udp:
                    return packet
        except:
             print("can't receive from port: {}".format(self.local_port))
             await asyncio.sleep(10)
