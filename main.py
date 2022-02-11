import asyncio

from transport import Transport
from udp_transport import Udp_socket
from can_transport import Vcan_socket

class Transport_manager:
    """Class for unit transport sockets.
    This class allows you to redirect massages to other sockets
    For add socket to redirect use function add_transport()
    """
    def __init__(self):
        self.main_loop = asyncio.get_event_loop()
        self.transport_list = []

    def add_transport(self, transport: Transport):
        """function for add transport

        Args:
            transport (Transport): created object inherited from Transport
        """
        self.transport_list.append(transport)

    async def listener(self, transport: Transport, times: int):
        """Redirect massages from transport object to other transports

        Args:
            transport (Transport): created object inherited from Transport
        """
        endlessly = False
        if times == 0:
            endlessly = True

        while times or endlessly: 
            if times != 0: times -= 1
            data = await transport.listen_data()
            if data != None:
                for transport_for_send in self.transport_list:
                    if transport_for_send != transport:
                        await transport_for_send.send_data(data)
        

    async def main(self):
        """Function for created class
        """
        for transport in self.transport_list:
            self.main_loop.create_task(self.listener(transport, 0))

    def start(self):
        """function for run listening
        """
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

