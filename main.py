import asyncio

from transport import Transport
from udp_transport import Udp_socket
from can_transport import Vcan_socket

class Transport_manager:
    def __init__(self):
        self.main_loop = asyncio.get_event_loop()
        self.transport_list = []

    def add_transport(self, transport: Transport):
        self.transport_list.append(transport)

    async def listener(self, transport: Transport):
        while True:
            data = await transport.listen_data()
            if data != None:
                for transport_for_send in self.transport_list:
                    if transport_for_send != transport:
                        await transport_for_send.send_data(data)
        

    async def main(self):
            for transport in self.transport_list:
                self.main_loop.create_task(self.listener(transport))

    def start(self):
        self.main_loop.run_until_complete(self.main())
        self.main_loop.run_forever()



if __name__ == '__main__':
    transport_manager = Transport_manager()

    vcan0 = Vcan_socket('vcan0')
    vcan1 = Vcan_socket('vcan1')

    udp0 = Udp_socket()

    transport_manager.add_transport(vcan0)
    transport_manager.add_transport(vcan1)
    transport_manager.add_transport(udp0)

    transport_manager.start()

