import asyncio
import socket
import struct

from anyio import create_udp_socket, create_connected_udp_socket

from transport import Transport

SOCKET_MAX_DATA_LENGTH = 8


class Udp_socket(Transport):
    def __init__(self, local_port: int = 2000, 
                remote_host: str = 'localhost', 
                remote_port: int = 2001):
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port


    async def send_data(self, data: bytes):
        async with await create_connected_udp_socket(family = socket.AF_INET, 
                                                    remote_host = self.remote_host, 
                                                    remote_port = self.remote_port, 
                                                    local_host = 'localhost',
                                                    local_port = self.local_port) as udp:

            print('send_data', data)
            await udp.send(data)
        

    async def listen_data(self):
        print('start listening')
        async with await create_udp_socket(family = socket.AF_INET, local_port = self.local_port, local_host = 'localhost') as udp:
            async for packet, _ in udp:
                return packet



async def main_async(udp_socket: Udp_socket):
    while True:
        data = await udp_socket.listen_data()
        print('data: ' , data)
        await udp_socket.send_data(data)

    


if __name__ == '__main__':
    udp_socket = Udp_socket()
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main_async(udp_socket))

