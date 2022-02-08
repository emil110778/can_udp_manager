import can
import asyncio

from transport import Transport

class Vcan_socket (Transport):
    def __init__(self, can_port: str = 'vcan0'):
        self.port = can_port
        self.bus = can.interface.Bus(self.port, bustype = 'socketcan')
    
    def encode_data(self, arbitration_id_type: bool, arbitration_id: int, is_remote_frame: bool, is_error_frame: bool, data: bytes):

        ret = list(data)

        ret.insert(0, (arbitration_id_type | (is_remote_frame << 1) | (is_error_frame << 2) | ((arbitration_id & 0b11111) << 3)))
        ret.insert(1, (arbitration_id >> 5) & 0xFF)

        if arbitration_id_type:
            ret.insert(2, (arbitration_id >> (5 + 8)) & 0xFF)
            ret.insert(3, (arbitration_id >> (5 + 8*2)) & 0xFF)

        return ret

    def decode_data(self, data: bytes):

        arbitration_id_type = bool(data[0] & 0b1)
        is_remote_frame = bool(data[0] & 0b01)
        is_error_frame = bool(data[0] & 0b001)
        
        arbitration_id = data.pop(0) >> 3
        arbitration_id |= data.pop(0) << 5

        if arbitration_id_type:
            arbitration_id |= data.pop(0) << (5 + 8)
            arbitration_id |= data.pop(0) << (5 + 8 * 2)

        return  arbitration_id_type, arbitration_id, is_remote_frame, is_error_frame, data

    async def send_data(self, data: bytes):

        arbitration_id_type, arbitration_id, is_remote_frame, is_error_frame, data = self.decode_data(data)

        massage = can.Message(is_extended_id = arbitration_id_type, 
            arbitration_id = arbitration_id, 
            data = data, 
            is_remote_frame = is_remote_frame, 
            is_error_frame = is_error_frame)
        self.bus.send(massage)
        

    
    async def listen_data(self):
        message = self.bus.recv(timeout = 0)
        ret = message if message == None else self.encode_data(arbitration_id_type = message.is_extended_id, 
            arbitration_id = message.arbitration_id, 
            is_remote_frame = message.is_remote_frame, 
            is_error_frame = message.is_error_frame, 
            data = message.data)
        if ret != None:
            print(message.is_extended_id, 
            message.arbitration_id, 
            message.is_remote_frame, 
            message.is_error_frame, 
            message.data)
        return ret


async def main_async(can_socket: Vcan_socket):
    while True:
        data = await can_socket.listen_data()
        if data != None:
            
            await udp_socket.send_data(data)

    


if __name__ == '__main__':
    udp_socket = Vcan_socket()
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main_async(udp_socket))